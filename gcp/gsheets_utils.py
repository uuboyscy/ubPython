"""
Credential for Google Sheets.

GoogleSheets API usage limits:
    https://developers.google.com/sheets/api/limits
"""

import json
import time
from pathlib import Path

import pandas as pd
import pygsheets
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from prefect_gcp.secret_manager import GcpSecret
from pygsheets.client import Client
from pygsheets.exceptions import WorksheetNotFound

from utils.logging_udf import get_logger

logger = get_logger(in_prefect=True)

# This id is from GoogleDrive folder
# https://drive.google.com/drive/folders/2pWyw5zJygiqPUYZ2Js1CwfQIvBVJRoB8
# The folder is used only for converting Excel to GoogleSheets
GOOGLE_DRIVE_PARENTS_FOLDER_ID = "2pWyw5zJygiqPUYZ2Js1CwfQIvBVJRoB8"


def get_google_sheet_client() -> Client:
    """Get Google Sheets client."""
    return pygsheets.authorize(
        service_account_json=GcpSecret.load("google-drive").read_secret(),
    )


def get_drive_service() -> Resource:
    """get_drive_service."""
    return build(
        "drive",
        "v3",
        credentials=Credentials.from_service_account_info(
            json.loads(GcpSecret.load("google-drive").read_secret()),
        ),
    )


def convert_excel_to_google_sheets(
    excel_file_path: str,
    google_sheets_name: str | None = None,
) -> str:
    """Upload excel file to GoogleSheets and return GoogleSheets ID."""
    drive_service = get_drive_service()

    if google_sheets_name is None:
        google_sheets_name = f"google_sheets_{time.time_ns()}"

    file_metadata = {
        "name": google_sheets_name,
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [GOOGLE_DRIVE_PARENTS_FOLDER_ID],
    }

    media = MediaFileUpload(
        excel_file_path,
        mimetype="application/vnd.ms-excel",
        resumable=True,
    )

    # Upload file to GoogleSheets
    # fileds reference: https://developers.google.com/drive/api/reference/rest/v3/files
    try:
        file = (
            drive_service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )
    except HttpError as err:
        logger.error(err.args)  # noqa: TRY400
        time.sleep(60)
        file = (
            drive_service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )

    return file.get("id")


def download_google_sheets_to_excel(
    google_sheets_id: str,
    output_excel_path: str,
) -> None:
    """Download GoogleSheets to Excel file."""
    drive_service = get_drive_service()

    request = drive_service.files().export_media(
        fileId=google_sheets_id,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Reference: https://stackoverflow.com/questions/36173356/
    # google-drive-api-download-files-python-no-files-downloaded
    with Path.open(output_excel_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        # downloader.next_chunk() returns state and done (True/False)
        while not downloader.next_chunk()[1]:
            continue


def load_dataframe_to_google_sheets_worksheet(
    df: pd.DataFrame,
    spreadsheet_url: str,
    worksheet_title: str,
    start_address: tuple[int, int],
    copy_head: bool = True,
) -> None:
    """
    Load DataFrame to GoogleSheets.

    The object-type-columns on GoogleSheets will be forced configured to TEXT.
    (object-type-columns: str and mixed-type contains str are considered "object")
    For following example, only column object_col will be configured as TEXT on GoogleSheets.
    >>> df = pd.DataFrame(
            {
                "int_col": [1, 2, 3],
                "object_col": [4, "8", 9.6],
                "float_col": [1, 2, 3.6],
            },
        )
    >>> print(df["int_col"].dtype == "object")  # False
    >>> print(df["object_col"].dtype == "object")  # True
    >>> print(df["float_col"].dtype == "object")  # False

    :param start_address:   (2, 1) denote writing data from 2nd row and column A on Worksheet
    """
    client = get_google_sheet_client()
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet_by_title(worksheet_title)

    # Used to generate a list of object-type-column range
    # e.g. ["A2:A524", "B2:B524", "D2:D524"]
    # worksheet.apply_format() effect only on row 2 to row 524 of column label A, etc.
    # Column index start from 1, e.g. pygsheets.Address((0, 1)).label -> A
    object_type_column_range_list = []
    for column_number, column_type in enumerate(df.dtypes):
        if column_type != "object":
            continue

        column_start_row_label = pygsheets.Address(
            (start_address[0], column_number + 1),
        ).label
        column_end_row_label = pygsheets.Address(
            (df.shape[0] + start_address[0] - 1, column_number + 1),
        ).label
        object_type_column_range_list.append(
            f"{column_start_row_label}:{column_end_row_label}",
        )

    # Upload Dataframe to let GoogleSheets generate new cells
    worksheet.set_dataframe(df=df, start=start_address, copy_head=copy_head)

    # Type of columns can be configured only if cells exist
    if object_type_column_range_list:
        worksheet.apply_format(
            object_type_column_range_list,
            format_info={
                "numberFormat": {
                    "type": pygsheets.FormatType.TEXT.value,
                },
            },
        )

        # Upload DataFrame again, then cells will follow the types configured in the last step
        worksheet.set_dataframe(df=df, start=start_address, copy_head=copy_head)


def e_gsheet_to_df(gsheet_url: str, worksheet_title: str | None = None) -> pd.DataFrame:
    """Return DataFrame from a specified Google Sheets worksheet."""
    gc = get_google_sheet_client()
    sheet = gc.open_by_url(gsheet_url)
    if worksheet_title:
        return sheet.worksheet_by_title(worksheet_title).get_as_df(numerize=False)
    return sheet.sheet1.get_as_df(numerize=False)


def copy_worksheet(
    gsheet_url: str,
    worksheet_title: str,
    new_worksheet_title: str = "",
    hidden_sheet: bool = False,
    replace_if_exists: bool = False,
) -> None:
    """copy_worksheet."""
    gc = get_google_sheet_client()
    sheet = gc.open_by_url(gsheet_url)

    if not new_worksheet_title:
        new_worksheet_title = worksheet_title + "_copy"

    try:
        # If copied worksheet exists, delete it
        if replace_if_exists:
            sheet.del_worksheet(
                sheet.worksheet_by_title(
                    new_worksheet_title,
                ),  # Check if the worksheet exists
            )
    except WorksheetNotFound:
        pass

    sheet.add_worksheet(
        title=new_worksheet_title,
        src_worksheet=sheet.worksheet_by_title(worksheet_title),
        index=len([0 for _ in sheet]),
    )

    if hidden_sheet:
        sheet.worksheet_by_title(new_worksheet_title).hidden = True

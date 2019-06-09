from urllib import request
import json
import os
import ssl

# used to fix Python SSL CERTIFICATE_VERIFY_FAILED
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


class WeatherAPI:

    def __init__(self, city_id, town_id):
        self.city_id = city_id
        self.town_id = town_id
        self.url_all_cities = 'https://works.ioa.tw/weather/api/all.json'
        self.url_get_towns_by_cities = 'https://works.ioa.tw/weather/api/cates/%s.json'     ###
        self.url_get_towns_information = 'https://works.ioa.tw/weather/api/towns/%s.json'   ###
        self.url_get_url = 'https://works.ioa.tw/weather/api/url.json'
        self.url_get_towns_weather = 'https://works.ioa.tw/weather/api/weathers/%s.json'    ###
        self.url_img_path_dir = json.loads(request.urlopen(self.url_get_url).read())['img']


    def getAllCities(self):
        data_city = request.urlopen(self.url_all_cities).read().decode('utf-8')
        data_city_dict = json.loads(data_city)

        return data_city_dict


    def getTown(self):
        data_towns = request.urlopen(self.url_get_towns_by_cities % (self.city_id)).read().decode('utf-8')
        data_towns_dict = json.loads(data_towns)

        return data_towns_dict


    def getTownInformation(self):
        data_towns_information = request.urlopen(self.url_get_towns_information % (self.town_id)).read().decode('utf-8')
        data_towns_information_dict = json.loads(data_towns_information)

        return data_towns_information_dict


    def getTownWeatherInformation(self):
        data_weather_information = request.urlopen(self.url_get_towns_weather % (self.town_id)).read().decode('utf-8')
        data_weather_information_dict = json.loads(data_weather_information)

        return data_weather_information_dict


    def getTownIDDict(self):
        town_id_dict = {}
        data_city_dict = self.getAllCities()

        for ct in data_city_dict:
            for tn in ct['towns']:
                town_id_dict['%s,%s' % (ct['name'], tn['name'])] = [ct['id'], tn['id']]

        return town_id_dict


    def getTownID(self, location_name = '中壢'):
        town_id_dict = self.getTownIDDict()
        for n in town_id_dict:
            if location_name in str(n):
                return town_id_dict[n][1]

        return 81



# Test
if __name__ == '__main__':

    location1 = WeatherAPI(8, 81)

    # Get all cities
    print('Get all cities :')
    print(location1.getAllCities())

    print()

    # Get towns by city
    print('Get towns by city ID :')
    print(location1.getTown())

    print()

    # Get towns information
    print('Get towns information by town ID :')
    print(location1.getTownInformation())
    print('Location image url : %s'%(location1.getTownInformation()['img']))

    print()

    # Get town weather
    print('Get town weather :')
    print(location1.getTownWeatherInformation())

    # Get image url of town weather status
    status = location1.url_img_path_dir + location1.getTownWeatherInformation()['img']
    print('Get image url of town weather status : %s'%(status))

    print()

    # Get town ID by name
    print('Get town ID by name dict :')
    print(location1.getTownIDDict())

    print()

    # Get town ID
    print('Get town ID :')
    print('中壢 : %s'%(location1.getTownID('中壢')))
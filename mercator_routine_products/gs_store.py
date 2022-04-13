import requests
import json
from time import sleep


class StoreRefresher:
    def __init__(self):
        self.host = 'http://193.136.129.239:8080/geoserver/rest'
        self.user = 'admin'
        self.passw = '8IzJQ#^KI7Jj'
        # TODO: Define here more workspaces/stores if needed!
        self.stores = {
            'mercator': {
                'chlorophyll_concentration', 'chlorophyll_observation_daily',
                'mass_concentration_of_suspended_matter_in_sea_wate', 'nitrate_concentration',
                'oxygen_concentration', 'phosphate_concentration', 'salinity_forecast_daily',
                'silicate_concentration', 'surface_height_forecast_daily', 'temperature_forecast_daily',
                'temperature_observation_daily', 'vector_speed_forecast_daily'
            },
            'regional_model': {
                'latest_hydro_model_babitonga', 'latest_hydro_model_cep', 'latest_hydro_model_prsc',
                'latest_hydro_model_regional', 'latest_wp_model_babitonga', 'latest_wp_model_cep',
                'latest_wp_model_prsc', 'latest_wp_model_regional'
            }
        }

    def refresh_stores(self):
        try:
            auth = requests.auth.HTTPBasicAuth(self.user, self.passw)
            requests.post(self.host + '/reload', auth=auth)
            for w in self.stores:
                for s in self.stores.get(w):
                    data = requests.get(self.host + '/workspaces/{0}/coveragestores/{1}'.format(w, s), auth=auth)
                    if data.status_code == 200:
                        r = requests.put(self.host + '/workspaces/{0}/coveragestores/{1}'.format(w, s), auth=auth,
                                     data=data.text, headers= {'Content-type': 'application/json'})
                        if r.status_code == 200:
                            print('Updated store {0}'.format(s))
                            sleep(1)
                        else:
                            print('Could not updated store {0}'.format(s))
                    else:
                        print('Could not fetch store {0}'.format(s))

            # Reload/Reset catalog
            # requests.post(self.host + '/reload', auth=auth)

        except requests.RequestException as e:
            print(e)
        except requests.ConnectionError as e:
            print(e)


if __name__ == '__main__':
    StoreRefresher().refresh_stores()


import geoip2.database

#preload the GeoLite2 database so sb wont be mad
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def get_geo_data(ip_address):
    try:
        response = reader.city(ip_address)
        return {
            'ip': ip_address,
            'country': response.country.iso_code,
            'region': response.subdivisions.most_specific.name
        }
    except geoip2.errors.AddressNotFoundError:
        return {'error': 'ip not found in database or your dumb ass messed something up'}
    except Exception as e:
        return {'error': str(e)}

def close_reader():
    reader.close()
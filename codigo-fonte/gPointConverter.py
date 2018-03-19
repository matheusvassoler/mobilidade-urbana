import utm

class GPointerConverteClass:

    def convertLatLngToUtm(latitude, longitude):

        # Convert latitude/longitude into UTM coordinates
        return utm.from_latlon(latitude, longitude)

    def convertUtmToLatLng(UTMEasting, UTMNorthing, UTMZone):
        ZONE_LETTERS = "CDEFGHJKLMNPQRSTUVWXX"
        # Convert UTM to Longitude/Latitude
        return utm.to_latlon(UTMEasting, UTMNorthing, UTMZone, ZONE_LETTERS)
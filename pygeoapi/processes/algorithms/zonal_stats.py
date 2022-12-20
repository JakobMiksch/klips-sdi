from shapely.geometry import shape
from rasterstats import zonal_stats, utils
import httplib2


def get_zonal_stats(cog_url, polygon_geojson, statistic_methods=['count', 'min', 'mean', 'max', 'median']):
    """
    Creates zonal statistics from a COG using a single polygon as input

    :param cog_url: the URL of the COG
    :param polygon_geojson: A single polygon as dict structured as GeoJSON in the same projection as the COG
    :param statistic_methods: An array of statistic method names
                  e.g. ['count', 'min', 'max', 'mean', 'sum', 'std', 'median', 'majority', 'minority', 'unique', 'range', 'nodata', 'nan']
                  defaults to ['count', 'min', 'mean', 'max', 'median']

    :returns A dict structured as GeoJSON with the input geometry and its zonal statistics as properties
    """

    # validate URL of COG
    try:
        # request HEAD of URL to check its existence without downloading it
        response = httplib2.Http().request(cog_url, 'HEAD')
        assert response[0]['status'] != 200
    except:
        raise Exception(
            'Provided URL does not exist or cannot be reached.')

    # validate provided statistic methods
    if not isinstance(statistic_methods, list):
        raise Exception(
            'Provided statistic methods are not structured as list')

    # convert list of statistic methods to string
    stats = ' '.join(statistic_methods)

    polygon = shape(polygon_geojson)
    if polygon.type != 'Polygon':
        raise Exception('Provided geometry is no polygon')

    return zonal_stats(
        polygon,
        cog_url,
        stats=stats, geojson_out=True
    )


def main():
    cog_url = "http://localhost/ecostress_3035_cog.tif"
    polygon_geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    4582923.56687590200454,
                    3117421.271846642717719
                ],
                [
                    4581124.431979617103934,
                    3115178.194573352113366
                ],
                [
                    4584278.759395182132721,
                    3114862.761831795331091
                ],
                [
                    4584278.759395182132721,
                    3114862.761831795331091
                ],
                [
                    4582923.56687590200454,
                    3117421.271846642717719
                ]
            ]
        ]
    }
    # stats = None
    result = get_zonal_stats(cog_url, polygon_geojson)
    print(result)


if __name__ == '__main__':
    main()
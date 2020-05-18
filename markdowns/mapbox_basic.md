## Instructions
It is fairly simple to set up a basic map using MapBox in Django.
1.  Add the necessary headers to HTML header file
2.  Login to MapBox website and navigate to [JK Web](https://www.mapbox.com/install/js/) page
3.  Choose *Use the MapBox CDN* and continue to follow instructions from there
4.  When the MapBox Access Token (MBAT) is shown, add that into *environment variables* instead of template page
5.  Call the MBAT in the Views.py
6.  Access the token in the template file
7.  Set settings & styles for the map

### header_noaa.html
```html
    <!-- MapBox -->
    <script src='https://api.mapbox.com/mapbox-gl-js/v1.8.1/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v1.8.1/mapbox-gl.css' rel='stylesheet' />
```

### .env
```
MAPBOX_ACCESS_TOKEN={put the access token here}
```

### views.py
```python
# this is mapbox test zooming in on Edmonton
def map_box_test(request):

    context = {
        'mapbox_access_token': os.environ.get('mapbox_access_token')
    }

    return render(request, 'pages/mapbox.html', context)
```

### mapbox.html
Call the MBAT here and then set the `style`, `center`, and `zoom` variables for a basic starter map.
```html
    <div class="d-flex justify-content-center">
        <div id="map" style="width: 800px; height: 600px;"></div>
    </div>

    <script>
        mapboxgl.accessToken = '{{ mapbox_access_token }}';
        var map = new mapboxgl.Map({
            container: 'map',
            //style: 'mapbox://styles/mapbox/satellite-streets-v11',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-113.4938, 53.5461],
            zoom: 10
        });
    </script>
```

## Links
[Tutorial](https://www.fullstackpython.com/blog/maps-django-web-applications-projects-mapbox.html)
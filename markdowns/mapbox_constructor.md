To follow the constructor function pattern for mapbox, certain parts need to go in different places, most particular the `map.on('load')` function.

### Constructor Function
This one is straight forward, as with most constructor functions, get parent, svg size and variables.
```javascript
// constructor function
MapUSA = function(_parentElement, _svgHeight, _svgWidth, _yVariable) {
    this.parentElement = _parentElement;
    this.svgHeight = _svgHeight;
    this.svgWidth = _svgWidth;
    this.yVariable = _yVariable;

    this.initVis();
}
```

### Initialize Function
Initialize function will instantiate the map (`mapboxgl.Map`). 
```javascript
// initVis!
MapUSA.prototype.initVis = function() {
    var vis = this;

    mapboxgl.accessToken = '{{ mapbox_access_token }}';
    vis.map = new mapboxgl.Map({
        container: 'map',
        //style: 'mapbox://styles/mapbox/satellite-streets-v11',
        //style: 'mapbox://styles/mapbox/streets-v11',
        style: 'mapbox://styles/mapbox/dark-v10',
        // style: 'mapbox://styles/mapbox/light-v10',
        center: [-96, 37.8],
        zoom: 3.5
    });

    vis.wrangleData();
}
```

### Wrangle Data
Wrangle data will take in the changes to the user interface and map dataset accordingly.
```javascript
// wrangleData
MapUSA.prototype.wrangleData = function () {
    var vis = this;

    // get new yVariable
    vis.yVariable = $('#data-type-select').val();

    vis.newData = stations.map(function (x) {
        //console.log(x)
        return {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: x.geometry.coordinates
            },
            properties: {
                title: x.properties[vis.yVariable]
            }
        }
    });

    vis.updateVis();
}
```

### Update Visualization
Although it is called update, it completely refreshes the map call, which is necessary based on how MapBox maps work. Thus the `map.on('load')` function goes here, and all associated functions for changed parameters (e.g. date slider, dataset selections) need to go INSIDE of it.
```javascript
// updateVis
MapUSA.prototype.updateVis = function () {
    var vis = this;

    vis.map.on('load', function() {
        vis.map.addSource('points', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: vis.newData
            }
        });
        vis.map.addLayer({
            id: 'points',
            type: 'symbol',
            source: 'points',
            layout: {
                // get the icon name from the source's "icon" property
                // concatenate the name to get an icon from the style's sprite sheet
                'icon-image': ['concat', ['get', 'icon'], '-15'],
                // get the title name from the source's "title" property
                'text-field': ['get', 'title'],
                'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                'text-offset': [0, 0],
                'text-anchor': 'top'
            },
            paint: {
                'text-color': 'red'
            }
        });
        //console.log(vis.map.getSource('points'));

        document.getElementById('data-type-select')
            .addEventListener('change', function() {
                vis.map.getSource('points').setData(updateData(vis.newData));
            })
    });
}
```

### Outside the constructors
The instantiation of the constructor and any changes in the user paramaters need to be handled outside of the constructors.
```javascript
// updateData
function updateData(theNewData) {
    return {
        type: 'FeatureCollection',
        features: theNewData
    };
}

// declare and call new MapUSA
var newMap;
newMap = new MapUSA('#map', 600, 1000, 'TMAX');

// update the map based on new variable
$("#data-type-select").on("change", function() {
    newMap.wrangleData();
});
```
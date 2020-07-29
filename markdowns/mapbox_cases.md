### Using Case Expressions
Case expressions help provide the filtering and interpolating of displayed data as needed. For example, in showing the temperature gradient, the case checks for a normalized temperature between 0 and 1. If this is true, then interpolate the value between 0 and 1. Otherwise, default as 'transparent/white'.

```javascript
    map.addLayer({
        id: 'hexagons-draw',
        type: 'fill',
        source: 'hexagons-draw',
        paint: {
            'fill-color':
                [
                    'case',
                    [">", ["get", "temperature"], 0],
                    [
                        "interpolate", ["linear"], ["get", "temperature"],
                            0, 'rgb(148,0,211)',
                            0.45, 'rgb(114,212,188)',
                            0.55, 'rgb(100, 255, 50)',
                            0.7, 'rgb(255, 255, 0)',
                            0.9, 'rgb(255, 0, 0)',
                            1, 'rgb(153, 0, 0)'
                    ],
                    'rgb(0, 0, 0)'
                ],
            'fill-opacity':
                [
                    'case',
                    [">", ["get", "temperature"], 0], 0.3,
                    0,
                ]
        }
    });

```

*  MapBox docs - [Case Expressions](https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#case)
*  [Set Default Value](https://stackoverflow.com/questions/49328075/mapbox-data-driven-style-setting-color-for-values-not-in-object)

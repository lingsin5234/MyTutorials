### Animate a point in MapBox
[Example](https://docs.mapbox.com/mapbox-gl-js/example/animate-point-along-line/)  
Use `setData` to apply the updated dataset to the map source
```javascript
vis.map.getSource('points').setData(updateData(vis.newData));
```

#### Possible error:
> map.getSource() is undefined
[link](https://stackoverflow.com/questions/46676189/call-map-getsource-setdata-results-in-typeerror-cannot-read-property)
This happens when calling the `getSource` outside of the `map.on('load')` function. The call needs to be done inside:
```javascript
vis.map.on('load', function() {

...
        vis.map.getSource('points').setData(updateData(vis.newData));
    })
});
```

### Call document elements to conduct changes
[Example](https://docs.mapbox.com/mapbox-gl-js/example/timeline-animation/)
Again, this needs to be done inside the `map.on('load')` function, call the element and make the associated changes as needed. Since we are using `on('load')`, the functions will be loaded at that time too, thus will execute each time there are changes to the associated elements (in below example, the 'slider').
```javascript
vis.map.on('load', function() {

...
    document
        .getElementById('slider')
        .addEventListener('input', function(e) {
        var month = parseInt(e.target.value, 10);
            filterBy(month);
        });
}
```
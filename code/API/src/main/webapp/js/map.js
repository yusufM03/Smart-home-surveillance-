$(document).ready(function () {
    // Base layer with OpenStreetMap
    const lyrOSM = new ol.layer.Tile({
        title: 'OSM',
        type: 'base',
        visible: true,
        source: new ol.source.OSM(),
    });

    // Map view configuration
    const mapView = new ol.View({
        projection: "EPSG:4326",
        center: [10.1874518, 36.8917497],
        zoom: 9,
    });

    // Layers list
    const layersList = [lyrOSM];

    // Define default styles
    const defaultStyle = new ol.style.Style({
        fill: new ol.style.Fill({ color: "rgba(255, 100, 50, 0.3)" }),
        stroke: new ol.style.Stroke({ width: 2, color: "rgba(255, 100, 50, 0.8)" }),
        image: new ol.style.Icon({
            src: 'https://cdn-icons-png.flaticon.com/512/6395/6395271.png',
            scale: 0.1,
        }),
    });

    // Initialize map
    const map = new ol.Map({
        target: 'map',
        layers: layersList,
        view: mapView,
    });

    // Home coordinates
    const homeCoordinates = [36.89205104519386, 10.187848998458026]; // Set your home coordinates here

    // Add home marker
    const homeMarker = new ol.Overlay({
        position: homeCoordinates,
        element: document.createElement('div'),
        positioning: 'center-center',
    });
    // Style the home marker
    homeMarker.getElement().style.width = '24px';
    homeMarker.getElement().style.height = '24px';
    homeMarker.getElement().style.backgroundImage = 'url(https://cdn-icons-png.flaticon.com/512/25/25694.png)';
    homeMarker.getElement().style.backgroundSize = 'contain';

    map.addOverlay(homeMarker);

    // Button: Reset zoom and fit map
    document.getElementById("button zoom").onclick = function () {
        map.getView().fit(map.getView().calculateExtent());
        map.getView().setZoom(0);
    };

    // Button: Center map on home location
    document.getElementById("button_home").onclick = function () {
        map.getView().setCenter(homeCoordinates);
        map.getView().setZoom(15);
    };

    // Button: Get user position
    document.getElementById("button_pos").onclick = function () {
        const geolocation = new ol.Geolocation({
            projection: map.getView().getProjection(),
            tracking: true,
        });

        // Marker for user location
        const marker = new ol.Overlay({
            element: document.getElementById("location"),
            positioning: "center-center",
        });
        map.addOverlay(marker);

        geolocation.on("change:position", function () {
            const position = geolocation.getPosition();
            if (position) {
                map.getView().setCenter(position);
                map.getView().setZoom(15);
                marker.setPosition(position);

                // Add marker as a feature
                const point = new ol.geom.Point(position);
                const vectorSource = new ol.source.Vector({ projection: "EPSG:4326" });
                const vectorLayer = new ol.layer.Vector({
                    source: vectorSource,
                    style: new ol.style.Style({
                        image: new ol.style.Icon({
                            src: 'https://cdn3.iconfinder.com/data/icons/maps-and-navigation-7/65/68-512.png',
                            scale: 0.1,
                        }),
                    }),
                });

                vectorSource.addFeature(new ol.Feature(point));
                map.addLayer(vectorLayer);
            }
        });
    };

    // Retrieve access token and mail from localStorage
    const accessToken = localStorage.getItem("accesstoken");
    const mail = localStorage.getItem("mail");
    const authorizationHeader = `Bearer ${accessToken}`;
    console.log(accessToken);



});

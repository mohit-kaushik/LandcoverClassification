var landsat8 = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR"),
    nlcd = ee.ImageCollection("USGS/NLCD"),
    region = 
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Feature(
        ee.Geometry.Polygon(
            [[[-96.64521229031749, 41.29211576900064],
              [-96.64521229031749, 36.4896178244455],
              [-82.62665760281749, 36.4896178244455],
              [-82.62665760281749, 41.29211576900064]]], null, false),
        {
          "system:index": "0"
        }),
    imageCollection = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA");

var image_landsat = imageCollection
                    .filterBounds(region.geometry())
                    .filterDate("2016-01-01","2016-12-30")
                    .filterMetadata("CLOUD_COVER","less_than",2)
                    .select(["B4","B3","B2","B7","B6","B5"])
                    .mosaic()
                    .clip(region.geometry())

Map.addLayer(image_landsat,{min:0,max:0.3},"landsat")


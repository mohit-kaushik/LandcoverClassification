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

// 11-21 water ice
// 22 -31 developed
// 41 - 81 green
// 90-95 wetlands

var nlcd_water_ice = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover')
                .lte(21)

var nlcd_dev1 = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover')
                .gte(22)

var nlcd_dev2 = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover')
                .lte(31)

var nlcd_dev = nlcd_dev1.and(nlcd_dev2)

var nlcd_green1 = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover')
                .gte(41)

var nlcd_green2 = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover')
                .lte(81)

var nlcd_green = nlcd_green1.and(nlcd_green2)

var nlcd_wetlands = ee.Image('USGS/NLCD/NLCD2016')
                .select('landcover').gte(90)

var nlcd_image = nlcd_water_ice
              .addBands(nlcd_dev)
              .addBands(nlcd_green)
              .addBands(nlcd_wetlands)
              .clip(region.geometry())
              
nlcd_image = nlcd_image.rename(['water','dev','vegi','wetland'])              
var combined =  nlcd_image.addBands(image_landsat)

Map.addLayer(combined,{},'nlcd lancover')



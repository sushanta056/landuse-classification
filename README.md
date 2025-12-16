This project implements a Land Use Classification model using XGBoost and is successfully deployed as a web application. 

Model Performance
-Accuracy: 98.13% and Confusion Matrix: 
  [[221, 0, 0, 0],  
   [0, 296, 1, 0],  
   [0, 3, 245, 5],  
   [0, 0, 11, 285]] on testing data.
   
It predicts land use classes like water, forest, agriculture and urban land from satellite images.

A sample data extraction script is provided below:
https://code.earthengine.google.com/fa6fbdf8703f3869fbed89f82f25e2b9

The model was trained on over 4,000 samples (approximately 1,000 per class) collected from the Pokhara Valley and nearby hilly regions.

Although NDVI, NDWI, and NDBI indices value were downloaded from GEE, they were not used during model training because they did not improve model accuracy.

This model is best suited for generating land use maps for Pokhara Valley and nearby hilly region, as it was trained on region-specific data.

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

These are the landuse map of my home city (Pokhara valley) which is generated using this model.
   <img width="1919" height="1024" alt="Screenshot 2025-12-17 012019" src="https://github.com/user-attachments/assets/501bbeca-326f-4bfb-92ba-89e3ae565d0b" />
   <img width="1919" height="1028" alt="Screenshot 2025-12-17 011959" src="https://github.com/user-attachments/assets/931e31ec-8b5f-4d9b-97ed-d3cb528da63d" />


The web application was deployed using HTML, CSS, JavaScript, and Flask.

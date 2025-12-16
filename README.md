This project implements a Land Use Classification model using XGBoost and is successfully deployed as a web application. 

Model Performance
-Accuracy: 98.13%
-Confusion Matrix (testing data): 
  [[221, 0, 0, 0],  
   [0, 296, 1, 0],  
   [0, 3, 245, 5],  
   [0, 0, 11, 285]]
   
It predicts land use classes like water, forest, agriculture and urban land from satellite images.

A sample data extraction script is provided below:
https://code.earthengine.google.com/2d4c8ef21af76a61c60d28c0cf6bf327

The model was trained on over 4,000 samples (approximately 1,000 per class) collected from the Pokhara Valley and nearby hilly regions.

This model is best suited for generating land use maps for Pokhara Valley and nearby hilly region, as it was trained on region-specific data.

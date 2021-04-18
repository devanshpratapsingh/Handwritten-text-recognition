import streamlit as st
import keras
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
import urllib.request
#from streamlit_drawable_canvas import st_canvas
import time

html_temp = '''
    <div style = "background-color: rgba(25,25,112,0.03); padding-bottom: 20px; padding-top: 20px; padding-left: 5px; padding-right: 5px">
    <center><h1>Handwritten Digit Recognition</h1></center>
    
    </div>
    '''
st.markdown(html_temp, unsafe_allow_html=True)
html_temp = '''
    <div>
    <h2></h2>
    <center><h3>Please upload Image for Classification</h3></center>
    </div>
    '''
st.set_option('deprecation.showfileUploaderEncoding', False)
st.markdown(html_temp, unsafe_allow_html=True)
opt = st.selectbox("How do you want to upload the image for classification?\n", ('Please Select', 'Upload image via link', 'Upload image from device', 'Draw the Digit!'))
if opt == 'Upload image from device':
    file = st.file_uploader('Select', type = ['jpg', 'png', 'jpeg'])
    st.set_option('deprecation.showfileUploaderEncoding', False)
    if file is not None:
        image = Image.open(file)

elif opt == 'Upload image via link':
  
  try:
    img = st.text_input('Enter the Image Address')
    image = Image.open(urllib.request.urlopen(img))
    
  except:
    if st.button('Submit'):
      show = st.error("Please Enter a valid Image Address!")
      time.sleep(4)
      show.empty()

elif opt == 'Draw the Digit!':
  b_width = st.slider('Brush Width: ',1,50,10)
  drawing_mode = st.checkbox("Draw",True)
  image_data = st_canvas(b_width, '#000', '#EEE', height=200,width=300, drawing_mode=drawing_mode, key="canvas")
  try:
    cv2.imwrite("test.jpg",image_data)
    image = Image.open("test.jpg")
  except:
    pass
try:
  if image is not None:
    st.image(image, width = 300, caption = 'Uploaded Image')
    if st.button('Predict'):
        model = keras.models.load_model('model/model.h5')
        image = np.array(image.resize((28, 28), Image.ANTIALIAS))
        image = np.array(image, dtype='uint8' )
        image = image[:,:,0]
        image = np.invert(np.array([image]))
        prediction = model.predict(image)
        st.success('Hey! The uploaded digit has been predicted as {}'.format(np.argmax(prediction)))

except:
  pass

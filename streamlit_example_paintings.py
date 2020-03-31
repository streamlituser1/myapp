import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
import requests

st.header('Playing With Famous Paintings')

st.sidebar.subheader('App options')
img_select = st.sidebar.selectbox('Choose painting', ('Nighthawks', 'Starry Night', 'The Persistence of Memory'))
treatment_select = st.sidebar.selectbox('Choose treatment', ('None','Gold frame','Color tint', 'Flip image'))

# Assigning URL and captions to image selection
if img_select == 'Nighthawks':
  caption = 'Nighthawks by Edward Hopper'
  img_url = 'https://cdn.britannica.com/42/19342-050-1034FC73/Nighthawks-oil-canvas-Edward-Hopper-Art-Institute-1942.jpg'
elif img_select == 'Starry Night':
  caption = 'Starry Night by Vincent Van Gogh'
  img_url = 'https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg'
elif img_select == 'The Persistence of Memory':
  caption = 'The Persistence of Memory by Salvador Dali'
  img_url = 'https://cdn.britannica.com/10/182610-050-77811599/The-Persistence-of-Memory-canvas-collection-Salvador-1931.jpg'

# Caching this function so that on subsequent runs the app will quickly load the selected image
@st.cache
def get_img_array(img_url):
  response = requests.get(img_url)
  img_fetch = Image.open(BytesIO(response.content))
  img_array = np.array(img_fetch) # Converting to a Numpy array so we can change individual pixels of the image
  img = Image.fromarray(img_array)
  return img, img_array

img, img_array = get_img_array(img_url)

if treatment_select == 'None':

  st.subheader('Here\'s the image with no treatment')
  st.write('To have some fun choose one of the treatments from the sidebar 🎈')
  st.image(img, caption=caption, width=500)

elif treatment_select == 'Gold frame':

  frame_size = st.slider('Change frame size', 10, 50)

  def framed_photo(df):
      img_array_framed = np.array(df)
      frame_color = [212,175,55]
      #frame_color = [55,212,175]
      img_array_framed[0:frame_size] = frame_color
      img_array_framed[-frame_size:] = frame_color
      img_array_framed[:,0:frame_size] = frame_color
      img_array_framed[:,-frame_size:] = frame_color
      img_framed = Image.fromarray(img_array_framed)
      caption_framed = str(caption) + ' properly framed'
      st.image(img_framed, caption=caption_framed, width=500)

  framed_photo(img_array)

elif treatment_select == 'Color tint':

  color_tint = st.selectbox('Choose color tint', ('','Red', 'Green', 'Blue'))

  def tint_image():
      if color_tint == 'Red':
          img_array_red = np.array(img_array).copy()
          img_array_red[:,:,0] = 185
          img_rosy = Image.fromarray(img_array_red)
          caption_red = str(caption) + ' wearing rose-colored glasses'
          st.image(img_rosy, caption=caption_red, width=500)
      elif color_tint == 'Green':
          img_array_green = np.array(img_array).copy()
          img_array_green[:,:,0] = 0
          img_underwater = Image.fromarray(img_array_green)
          caption_green = str(caption) + ' as seen from underwater'
          st.image(img_underwater, caption=caption_green, width=500)
      elif color_tint == 'Blue':
          img_array_blue = np.array(img_array).copy()
          img_array_blue[:,:,2] = 220
          img_cold = Image.fromarray(img_array_blue)
          caption_blue = str(caption) + ' on a cold winter\'s day'
          st.image(img_cold, caption=caption_blue, width=500)
      else:
          st.image(img, caption=caption, width=500)

  tint_image()


elif treatment_select == 'Flip image':

  flip_direction = st.radio('Select flip direction', ('Normal', 'Horizontal', 'Vertical'))

  if flip_direction == 'Normal':
      st.image(img, caption=caption, width=500)
  elif flip_direction == 'Horizontal':
      img_array_flip = np.flip(img_array, 1)
      img_flip = Image.fromarray(img_array_flip)
      caption_flip = str(caption) + ' flipped horizontally'
      st.image(img_flip, caption=caption_flip, width=500)
  elif flip_direction == 'Vertical':
      img_array_flip = np.flip(img_array, 0)
      img_flip = Image.fromarray(img_array_flip)
      caption_flip = str(caption) + ' flipped vertically'
      st.image(img_flip, caption=caption_flip, width=500)

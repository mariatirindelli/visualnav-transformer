import imfusion
import argparse

import pickle as pkl
import os
from pyquaternion import Quaternion
import numpy as np
from typing import Any, Tuple, List, Dict
from scipy.spatial.transform import Rotation as R
from PIL import Image

def load_imf_us(file_path):

    return_list = []

    imfusion_data = imfusion.load(file_path)
    if (len(imfusion_data) == 0):
        print("File: ", imfusion_data, " empty")
        return []
    
    for us in imfusion_data:
        if not isinstance(us, imfusion.TrackedSharedImageSet):
            continue
        return_list.append(us)  
        

    return return_list 
        
# TODO: add eventual processing of the image

# PROCESS_IMAGES_FUNCTIONS
def dummy_image_proc(image):
    return image
 
def convert_to_PIL(imf_image):
    img_array = np.squeeze(np.array(imf_image))
    return Image.fromarray(img_array)

# PROCESS ODOM FUNCTIONS
def nav_to_xyz_angles(traj)-> Dict[np.ndarray, np.ndarray]:
    position = traj[0:3, 3]
    xyz_angles = R.from_matrix(traj[0:3, 0:3]).as_euler("xyz", degrees=True)
    return position, np.array(xyz_angles)

# -----------------------------------------
def process_odom(
    traj_list: List,
    odom_process_func: Any,
) -> Dict[np.ndarray, np.ndarray]:
    """
    Process odom data from a topic that publishes nav_msgs/Odometry into position and yaw
    """
    xyz_positions = []
    xyz_angles = []
    for traj in traj_list:
        pos, angles = odom_process_func(traj)
        xyz_positions.append(pos)
        xyz_angles.append(angles)
    return {"position": np.array(xyz_positions), "xyz_angles": np.array(xyz_angles)}

def process_images(im_list: List, img_process_func) -> List:
    """
    Process image data from a topic that publishes ros images into a list of PIL images
    """
    images = []
    for img_msg in im_list:
        img = img_process_func(img_msg)
        images.append(img)
    return images


# equivalent to filter_backword, to split the trajectory into small chunks to avoid things like bacword motions or i.e. in case of US it could be
# decoupling from skin or sudden motions
def filter_and_cut( img_list: List[Image.Image],
    traj_data: Dict[str, np.ndarray],
    start_slack: int = 0,
    end_slack: int = 0,
) -> Tuple[List[np.ndarray], List[int]]:
    
    # dummy function, not doing anything
    return [(img_list, traj_data)]



def get_images_and_trajectories(
    tracked_img : imfusion.TrackedSharedImageSet,
    config
):
    """
    Get image and odom data from a bag file

    Args:
        bag (rosbag.Bag): bag file
        imtopics (list[str] or str): topic name(s) for image data
        odomtopics (list[str] or str): topic name(s) for odom data
        img_process_func (Any): function to process image data
        odom_process_func (Any): function to process odom data
        rate (float, optional): rate to sample data. Defaults to 4.0.
        ang_offset (float, optional): angle offset to add to odom data. Defaults to 0.0.
    Returns:
        img_data (list): list of PIL images
        traj_data (list): list of odom data
    """
        
    if (len(tracked_img) == 0):
        print("File: ", tracked_img, " empty")
        return []
        
    trajs = []
    imgs = []
    for i in range(tracked_img.size):
        mat = tracked_img.matrix(i)
        img = tracked_img[i]
        imgs.append(img)
        trajs.append(mat)

    img_data = process_images(imgs, convert_to_PIL)
    traj_data = process_odom(
        trajs,
        nav_to_xyz_angles,
    )

    return img_data, traj_data

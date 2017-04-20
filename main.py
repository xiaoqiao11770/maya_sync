import os
import shutil
import maya.cmds as cmds
import pymel.core as pm

def run():
    path_env = 'CWT_TEMP_ROOT_PATH'
    packet_path = 'C:/Users/jon/Documents/packet'
    os.environ[path_env] = packet_path
    path_env = '$' + path_env
    if not os.path.isdir(packet_path):
        os.mkdir(packet_path)

    shader_dir = os.path.join(packet_path, 'shader_img')
    env_shader_dir = path_env + '/' + 'shader_img'
    reference_dir = os.path.join(packet_path, 'reference')
    env_reference_dir = path_env + '/' + 'reference'
    cam_img_dir = os.path.join(packet_path, 'cam_img')
    env_cam_dir = path_env + '/' + 'cam_img'

    for dir in (shader_dir, reference_dir, cam_img_dir):
        if not os.path.isdir(dir):
            os.mkdir(dir)

    file_paths = []

    ref_list = pm.ls(type='reference')
    # For each file node..
    for f in ref_list:
        if f.name() != 'sharedReferenceNode':
            ref_path = f.referenceFile().path
            file_name = os.path.basename(ref_path)
            new_file = os.path.join(reference_dir, file_name)
            if os.path.isfile(ref_path):
                if not os.path.exists(new_file):
                    shutil.copy(ref_path, reference_dir)
                env_new_file = env_reference_dir + '/' + file_name
                f.referenceFile().load(env_new_file)
                file_paths.append(ref_path)

    shader_list = cmds.ls(type='file')
    for i in shader_list:
        texture_filename = cmds.getAttr(i + '.fileTextureName')
        if os.path.isfile(texture_filename):
            file_name = os.path.basename(texture_filename)
            new_file = os.path.join(shader_dir, file_name)
            if not os.path.isfile(new_file):
                shutil.copy(texture_filename, shader_dir)
            env_new_file = env_shader_dir + '/' + file_name
            cmds.setAttr(i + '.fileTextureName', env_new_file, type='string')
            file_paths.append(texture_filename)

    cam_img_list = cmds.ls(type='imagePlane')
    for c in cam_img_list:
        img_file = cmds.getAttr(c + '.imageName')
        if os.path.isfile(img_file):
            file_name = os.path.basename(img_file)
            new_file = os.path.join(cam_img_dir, file_name)
            if not os.path.isfile(new_file):
                shutil.copy(img_file, cam_img_dir)
            env_new_file = env_cam_dir + '/' + file_name
            cmds.setAttr(c + '.imageName', env_new_file, type='string')
            file_paths.append(img_file)

    current_name = cmds.file(q=1, sceneName=1)
    new_file = os.path.join(packet_path, os.path.basename(current_name))
    cmds.file(rename=new_file)
    cmds.file(save=True)


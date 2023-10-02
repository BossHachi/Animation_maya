# -*- coding: utf-8 -*-

import maya.cmds as cmds

def bake_frames(frame_interval, keep_frames):
    selected_objs = cmds.ls(selection=True)

    if not selected_objs:
        cmds.warning("There are no selected objects")
        return

    # 移動値と回転値のみアニメーションベイク
    st = int(cmds.playbackOptions(min=1, q=1))
    ed = int(cmds.playbackOptions(max=1, q=1))

    cmds.ogs(pause=True)
    cmds.bakeResults(selected_objs, sm=True, t=(st, ed), at=["tx", "ty", "tz", "rx", "ry", "rz"])
    cmds.ogs(pause=True)

    # フレーム数の倍数をリスト化する
    frame_list = [ed, ]  # エンドフレームは残す
    for i in range(st, ed + 1):
        if i % frame_interval == 0:
            frame_list.append(i)

    if keep_frames:
        keep_frames = keep_frames.split(',')
        for frame in keep_frames:
            frame = frame.strip()
            if frame.isdigit():
                frame_list.append(int(frame))

    # 選択されたすべてのリグに対して一括でアニメーションキーを削除
    for obj in selected_objs:
        keys = cmds.keyframe(obj, q=True)
        if keys:
            for key in keys:
                if key not in frame_list:
                    cmds.cutKey(obj, time=(key, key))

def create_gui():
    if cmds.window("bake_frames_window", exists=True):
        cmds.deleteUI("bake_frames_window")

    cmds.window("bake_frames_window", title="BakeFramer")
    cmds.columnLayout(adj=True)
    cmds.text(label="Enter the frame interval to delete.")
    frame_field = cmds.intField(minValue=1, value=5)
    
    cmds.text(label="Input frames to keep, separated by commas.")
    keep_frame_field = cmds.textField()
    
    bake_button = cmds.button(label="Bake", command=lambda _: bake_frames(cmds.intField(frame_field, q=True, v=True), cmds.textField(keep_frame_field, q=True, text=True)))
    cmds.showWindow()

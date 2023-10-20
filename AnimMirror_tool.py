import maya.cmds as cmds

selected_rigs = None

def mirror_start(*args):
    global selected_rigs      
    selected_rigs = cmds.ls(selection=True)
    
    cmds.currentTime(-1)
    cmds.move(0, 0, 0, selected_rigs, ls = True)
    cmds.rotate(0, 0, 0, selected_rigs)
    cmds.setKeyframe(selected_rigs)
        
    target_loc_list = []
    Match_rigloc_list = []
    set_list = []
    bake_loc_del =[]
    
    null_create = cmds.CreateEmptyGroup()
    cmds.rename(null_create,'inversion_loc')
        
    for rig in selected_rigs:
        trLocked = cmds.getAttr(rig + ".translateX", lock=True) and \
                        cmds.getAttr(rig + ".translateY", lock=True) and \
                        cmds.getAttr(rig + ".translateZ", lock=True)
        rtLocked = cmds.getAttr(rig + ".rotateX", lock=True) and \
                         cmds.getAttr(rig + ".rotateY", lock=True) and \
                         cmds.getAttr(rig + ".rotateZ", lock=True)
        # 回転値がロックされていて移動値がロックされていない場合の処理
        if rtLocked and not trLocked:                     
            point_name = rig + "_point"
            point_name = point_name.replace("right", "dummy")
            point_name = point_name.replace("left", "right" )
            point_name = point_name.replace("dummy", "left")
            point_base = cmds.spaceLocator(name = point_name)[0]
            cmds.matchTransform(point_base, rig, pos=True, rot=True)
            cmds.parent(point_base, rig)     
            target_loc_list.append(point_base)
            
        # 移動値がロックされていて回転値がロックされていない場合の処理
        elif trLocked and not rtLocked:
            orient_name = rig + "_orient"
            orient_name = orient_name.replace("right", "dummy")
            orient_name = orient_name.replace("left", "right" )
            orient_name = orient_name.replace("dummy", "left")    
            orient_base = cmds.spaceLocator(name = orient_name)[0]
            cmds.matchTransform(orient_base, rig, pos=True, rot=True)
            cmds.parent(orient_base, rig)    
            target_loc_list.append(orient_base)
            
        # 移動値と回転値がロックされていない場合の処理
        if not trLocked and not rtLocked:
            point_name = rig + "_point"
            point_name = point_name.replace("right", "dummy")
            point_name = point_name.replace("left", "right" )
            point_name = point_name.replace("dummy", "left")
            point_base = cmds.spaceLocator(name = point_name)[0]
            cmds.matchTransform(point_base, rig, pos=True, rot=True)            
                
            orient_name = rig + "_orient"
            orient_name = orient_name.replace("right", "dummy")
            orient_name = orient_name.replace("left", "right" )
            orient_name = orient_name.replace("dummy", "left")    
            orient_base = cmds.spaceLocator(name = orient_name)[0]
            cmds.matchTransform(orient_base, rig, pos=True, rot=True)
            cmds.parent(point_base, orient_base, rig) 
            
            target_loc_list.append(point_base)
            target_loc_list.append(orient_base) 

    for sel in target_loc_list:    
        loc_name = sel + "_bake"
        loc = cmds.spaceLocator(name=loc_name)[0]
        Match_rigloc_list.append(loc)
        
        pos = cmds.xform(sel, q=True, ws=True, translation=True)
        rot = cmds.xform(sel, q=True, ws=True, rotation=True)
        cmds.matchTransform(loc, sel, pos=True, rot=True)
        
        bake_loc = cmds.parentConstraint(sel, loc, mo=True)
        bake_loc_del.append(bake_loc)

    
    st = int(cmds.playbackOptions(min=1, q=True))
    ed = int(cmds.playbackOptions(max=1, q=True))
    
    cmds.ogs(pause=True)
    cmds.bakeResults(Match_rigloc_list, sm=True, t=(st-1, ed), at=["tx", "ty", "tz", "rx", "ry", "rz"])
    cmds.ogs(pause=True)

    for constraint in bake_loc_del:
        cmds.delete(constraint)
        
    cmds.parent(Match_rigloc_list,'inversion_loc')        
        
    cmds.delete(target_loc_list)
    cmds.setAttr('inversion_loc.scaleX', -1)
  
    Match_rigloc_list.extend(selected_rigs)

    for rig_name in selected_rigs:
        all_list = [s for s in Match_rigloc_list if rig_name in s]
        set = cmds.sets(all_list, n="matching_set_00")
        set_list.append(set)
    
    
    for set in set_list:
        # セット内のメンバーを取得
        set_members = cmds.sets(set, q=True)
    
        rig = None
        loc_point = None
        loc_orient = None
    
        # セット内のメンバーをループして条件に合致するものを検索
        for member in set_members:
            if member.startswith("MoxRig_rig_") and not member.endswith("_bake"):
                rig = member
            elif "point_bake" in member:
                loc_point = member
            elif "orient_bake" in member:
                loc_orient = member
    
        # ポイントコンストレイントとエイムコンストレイントを設定
        if rig and loc_point:
            cmds.pointConstraint(loc_point, rig, mo=False)

        if rig and loc_orient:
            cmds.orientConstraint(loc_orient, rig, mo=True)
        
        elif loc_orient:
            print("not orient",rig)
                
    cmds.currentTime(0)     

def mirror_bake(*args):
    global selected_rigs
    st = int(cmds.playbackOptions(min=1, q=True))
    ed = int(cmds.playbackOptions(max=1, q=True))    
    cmds.ogs(pause=True)
    cmds.bakeResults(selected_rigs, sm=True, t=(st, ed), at=["tx", "ty", "tz", "rx", "ry", "rz"])
    cmds.ogs(pause=True)
    
    for rig in selected_rigs:
        cmds.filterCurve(rig, f='euler')

    fcurve_list = cmds.keyframe(selected_rigs, q=True, n=True)
    for fcurve in range(3):
        for fcurve in fcurve_list:
            if fcurve.count('rotate'):
                hoge =cmds.keyframe(fcurve, q=True, vc=True)
                maxv = max(hoge)
                minv = min(hoge)
                if maxv > 180:   
                    cmds.keyframe(fcurve,e=True,r=True,vc=-360)
                    print(fcurve + u"を-360オフセットしました。")
                elif minv < -180:
                    cmds.keyframe(fcurve,e=True,r=True,vc=360)
                    print(fcurve + u"を-360オフセットしました。")
    
    cmds.currentTime(1)
    cmds.currentTime(0)
        

def mirror_Cleanup(*args):   
    cmds.delete('inversion_loc*')
    matching_sets = cmds.ls("matching_set*", type="objectSet")
    if matching_sets:
        cmds.delete(matching_sets)
    else:
        print("no matching_sets")
            
    cmds.currentTime(0)

def mirror_tool_gui():
    if cmds.window("Mirror_tool", exists=True):
        cmds.deleteUI("Mirror_tool")
         
    cmds.window("Mirror_tool", title="Mirror_tool")
    cmds.columnLayout(adj=True)
    cmds.separator()
    cmds.button(label="Mirror", command= mirror_start)
    cmds.separator()
    cmds.button(label="Bake", command= mirror_bake)
    cmds.separator()    
    cmds.button(label="Cleanup", command= mirror_Cleanup)
    cmds.separator()      
    cmds.showWindow()

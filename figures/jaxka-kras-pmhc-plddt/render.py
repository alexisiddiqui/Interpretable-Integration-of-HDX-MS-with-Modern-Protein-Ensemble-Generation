"""Render the PyMOL cartoon meshes with a shared orthographic Blender camera."""
from pathlib import Path
import bpy, numpy as np, json, math, sys
from mathutils import Vector
root=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast' if False else 'None'
scene.world.color=(0.65,0.65,0.65)
mat=bpy.data.materials.new('pLDDT');mat.use_nodes=True
nodes=mat.node_tree.nodes;bsdf=nodes.get('Principled BSDF');bsdf.inputs['Roughness'].default_value=.65;bsdf.inputs['Specular IOR Level'].default_value=.18
attribute=nodes.new('ShaderNodeVertexColor');attribute.layer_name='plddt';mat.node_tree.links.new(attribute.outputs['Color'],bsdf.inputs['Base Color'])
objects=[];allv=[]
for name in ['mutant','wt','empty']:
 d=np.load(root/(name+'-mesh.npz'));v=d['vertices'];f=d['triangles'];c=d['colors'];allv.append(v)
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update()
 color=mesh.color_attributes.new(name='plddt',type='FLOAT_COLOR',domain='POINT')
 linear=np.where(c<=.04045,c/12.92,((c+.055)/1.055)**2.4);rgba=np.c_[linear,np.ones(len(c))].astype(np.float32)
 color.data.foreach_set('color',rgba.ravel())
 obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(mat)
 for face in mesh.polygons:face.use_smooth=True
 objects.append(obj)
v=np.concatenate(allv);lo=v.min(axis=0);hi=v.max(axis=0);center=(lo+hi)/2
camera_data=bpy.data.cameras.new('Camera');camera=bpy.data.objects.new('Camera',camera_data);bpy.context.collection.objects.link(camera)
camera.location=(float(center[0]),float(center[1]),float(hi[2]+250));camera.rotation_euler=(0,0,0);camera.data.type='ORTHO'
camera.data.ortho_scale=max(float(hi[1]-lo[1]),float(hi[0]-lo[0])*1050/900)*1.12
scene.camera=camera
for name,offset,power,size in [('Key',(-80,120,150),180000,100),('Fill',(100,20,120),90000,120)]:
 light_data=bpy.data.lights.new(name,'AREA');light_data.energy=power;light_data.shape='DISK';light_data.size=size
 obj=bpy.data.objects.new(name,light_data);bpy.context.collection.objects.link(obj);obj.location=Vector(center)+Vector(offset);obj.rotation_euler=(Vector(center)-obj.location).to_track_quat('-Z','Y').to_euler()
(root/'scene.json').write_text(json.dumps({'blender_version':bpy.app.version_string,'camera_location':list(camera.location),'ortho_scale_angstrom':camera.data.ortho_scale,'frame_bounds':[lo.tolist(),hi.tolist()],'resolution':[900,1050],'samples':48,'engine':'Cycles CPU'},indent=2)+'\n')
for obj in objects:
 for other in objects:other.hide_render=other!=obj
 scene.render.filepath=str(root/(obj.name+'.png'));bpy.ops.wm.save_as_mainfile(filepath=str(root/(obj.name+'.blend')),compress=True);bpy.ops.render.render(write_still=True)

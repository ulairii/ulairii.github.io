#!/usr/bin/env python3
"""Original schematic comparisons for the condensed paper series; Python stdlib."""
from pathlib import Path
from html import escape
import textwrap
OUT = Path(__file__).resolve().parents[2] / 'images/driving-papers'
FIGURES = [
 ('Image perception: where the work happens', [
  ('R-CNN', ['Image regions', 'CNN per region', 'Boxes + classes']),
  ('Faster R-CNN', ['Shared features', 'Learned proposals', 'Refined boxes']),
  ('FCN', ['Image features', 'Spatial upsampling', 'Pixel labels'])]),
 ('Lidar: encoding and prediction are separate choices', [
  ('PointNet', ['Unordered points', 'Shared function', 'Symmetric pooling']),
  ('PointPillars', ['Points in columns', 'BEV features', '2D backbone']),
  ('CenterPoint head', ['Spatial features', 'Center heatmap', 'Size + pose + speed'])]),
 ('Two directions for camera-to-BEV transformation', [
  ('Lift-Splat-Shoot', ['Image features', 'Depth-weighted lift', 'Pool into BEV']),
  ('BEVDepth', ['Camera information', 'Supervised depth', 'Depth-guided BEV']),
  ('BEVFormer', ['BEV queries', 'Image + past BEV', 'Updated BEV'])]),
 ('Queries retrieve evidence for object hypotheses', [
  ('DETR3D', ['3D references', 'Project to images', 'Refine object queries']),
  ('PETR', ['3D coordinates', 'Position-aware images', 'Object queries']),
  ('Sparse4D', ['Instance state', 'Multi-view + time', 'Updated instances'])]),
 ('Fusion: choose where the sensor streams meet', [
  ('PointPainting', ['Image class scores', 'Attach to lidar points', 'Lidar detector']),
  ('BEVFusion: camera branch', ['Camera images', 'Camera BEV', 'Shared fusion']),
  ('BEVFusion: lidar branch', ['Lidar points', 'Lidar BEV', 'Shared fusion'])]),
 ('Scene structure: identity, shape, and connectivity', [
  ('Tracking', ['Previous tracks', 'Match observations', 'Updated identities']),
  ('MapTR', ['Sensor features', 'Map queries', 'Vector road shapes']),
  ('Topology task', ['Road elements', 'Predict relationships', 'Connected road graph'])]),
 ('Occupancy: present geometry versus future motion', [
  ('3D occupancy', ['Camera features', 'Spatial volume', 'Occupied / free cells']),
  ('FIERY', ['Camera history', 'Probabilistic future', 'BEV instances']),
  ('Occupancy flow', ['Scene history', 'Time-indexed grid', 'Occupancy + motion'])]),
 ('Motion prediction: structure and alternative futures', [
  ('VectorNet', ['Map + trajectories', 'Polyline encoding', 'Global interaction']),
  ('LaneGCN', ['Lane graph + actors', 'Structured interaction', 'Possible trajectories']),
  ('MTR', ['Scene features', 'Intention queries', 'Refined motion modes'])]),
 ('Planning: what generates and ranks trajectories?', [
  ('Search / sampling', ['Scene + constraints', 'Feasible candidates', 'Designed objective']),
  ('Neural Motion Planner', ['Lidar + HD map', 'Learned cost volume', 'Score candidates']),
  ('ChauffeurNet', ['Structured scene', 'Imitation + recovery', 'Predicted motion'])]),
 ('End-to-end driving can retain intermediate tasks', [
  ('TransFuser', ['Images + lidar', 'Attention fusion', 'Waypoints']),
  ('UniAD: scene tasks', ['Camera BEV', 'Tracks + map', 'Motion + occupancy']),
  ('UniAD: driving', ['Task features', 'Trajectory planning', 'Controller'])]),
 ('Compact scenes and generative actions', [
  ('VAD', ['Agent + map vectors', 'Scene interaction', 'Planned trajectory']),
  ('DiffusionDrive', ['Noisy motion anchors', 'Scene-guided denoising', 'Trajectory candidates']),
  ('System decision', ['Candidate set', 'Rank / select', 'Execute motion'])]),
 ('Evaluation: what responds to the planned action?', [
  ('Open loop', ['Recorded scene', 'Predicted trajectory', 'Compare with log']),
  ('Non-reactive rollout', ['Recorded actors', 'Advance ego vehicle', 'Score interaction']),
  ('Interactive rollout', ['Simulated scene', 'Ego + actors respond', 'Observe and replan'])]),
]
def draw():
 OUT.mkdir(parents=True,exist_ok=True)
 for n,(title,rows) in enumerate(FIGURES,1):
  parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 460" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">'+escape('; '.join(name+': '+' → '.join(boxes) for name,boxes in rows))+'</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#526577"/></marker></defs><rect width="760" height="460" fill="#fff"/><g font-family="Arial, sans-serif" fill="#24292e">']
  parts.append(f'<text x="22" y="34" font-size="23" font-weight="700">{escape(title)}</text>')
  for row,(label,boxes) in enumerate(rows):
   y=80+row*122
   parts.append(f'<text x="22" y="{y}" font-size="21" font-weight="600">{escape(label)}</text>')
   for col,value in enumerate(boxes):
    x=22+col*246
    parts.append(f'<rect x="{x}" y="{y+14}" width="222" height="70" rx="3" fill="'+('#eef3f7' if col==2 else '#fafafa')+'" stroke="#b7c2cc"/>')
    lines=textwrap.wrap(value,width=20)
    for j,line in enumerate(lines):
     parts.append(f'<text x="{x+111}" y="{y+55-(len(lines)-1)*12+j*24}" text-anchor="middle" font-size="21">{escape(line)}</text>')
    if col<2:parts.append(f'<path d="M{x+224} {y+49}h18" stroke="#526577" stroke-width="2" marker-end="url(#arrow)"/>')
  parts.append('<text x="22" y="445" font-size="17" fill="#555e67">Conceptual comparison; arrows summarize information flow.</text></g></svg>')
  (OUT/f'{n:02d}.svg').write_text(''.join(parts)+'\n')
if __name__=='__main__':draw()

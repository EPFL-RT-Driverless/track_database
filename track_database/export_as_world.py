import pandas as pd
from pathlib import Path
from typing import List
from xml.dom.minidom import parseString
from dict2xml import dict2xml


class WorldElement():
    """An element is an object populating a world file.
    Check the gazebo documentation for more details on required structure
    """
    def __init__(self, name: str, pose: list, count: int):
        """
        Args:
            name (str): the name of the element
            pose (list): the xyz position of the element
            count (Union[int, None]): the id of the element (unique) if int. 
                If None, must be the only occurence of this type 
        """
        self._model_uri = self._map_model_uri(name)
        self._name = self._map_name(name) + str(count)
        self._pose = self._map_pose(pose)

    @property
    def name(self):
        return self._name
    
    @property
    def model_uri(self):
        return self._model_uri

    @property
    def pose(self):
        return self._pose

    @staticmethod
    def _map_name(name: str) -> str:
        return name + '_cone'
        
    @staticmethod
    def _map_model_uri(name: str) -> str:
        name_ = 'orange_cone' if 'orange' in name else name + '_cone'
        return 'model://' + name_
    
    @staticmethod
    def _map_pose(pose: List[float]) -> str:
        pose.extend([0, 0, 0])
        return ' '.join([str(_) for _ in pose])
    
    def to_dict(self) -> dict:
        return {"include": {
            "uri": self._model_uri,
            "name": self._name,
            "pose": self._pose
        }} 


class TrackParser():
    """
    This class provides methods to build a world file compatible with gazebo
    based on a csv file FSDS compatible.
    """
    PATH_TO_DATABASE = Path(__file__).parent / 'data'
    def __init__(self, track_name: str, add_sun: bool = True, add_ground: bool = True):
        self.track_name = track_name
        self.add_sun = add_sun
        self.add_ground = add_ground
        self.cones = self._read_csv(track_name) 
        self.cone_types = set(self.cones.cone_type)
        self.elements = []
        self._extract_cone_information()
        self._to_dict()
        
        self._to_xml()
        self._wrap_xml('world', 'name', 'acceleration')
        self._wrap_xml('sdf', 'version', '1.4')
        self._clean_xml()

    def _read_csv(self, track_name: str) -> pd.DataFrame:
        track_folder_path = self.PATH_TO_DATABASE / track_name
        cone_positions = track_name + '_cones.csv'
        return pd.read_csv(track_folder_path / cone_positions)

    def _extract_cone_information(self):
        for cone_type in self.cone_types:
            for index, cone in self.cones[self.cones.cone_type == cone_type].reset_index().iterrows():
                element = WorldElement(cone_type, [cone.X, cone.Y, cone.Z], index)
                self.elements.append(element)

    def _to_dict(self) -> None:
        self.elements = [element.to_dict() for element in self.elements]
        if self.add_sun:
            self.elements.append(self._add_sun())
        if self.add_ground:
            self.elements.append(self._add_ground())

    def _to_xml(self):
        self._xml = '\n'.join([dict2xml(element, indent = ' ') for element in self.elements])
    
    def _wrap_xml(self, wrapper_name: str, special_tag: str, special_tag_value: str) -> str:
        wrapper_begin = f"""<{wrapper_name} {special_tag}="{special_tag_value}">\n"""
        wrapper_end = f"""\n</{wrapper_name}>"""
        self._xml = wrapper_begin + self._xml + wrapper_end

    @staticmethod
    def _add_sun() -> dict:
        return {"include": {"uri": "model://sun"}} 
    
    @staticmethod 
    def _add_ground() -> dict:
        return {"include": {"uri": "model://dry_plane"}}
    
    def _add_xml_version(self) -> None:
        xml_tag = """<?xml version="1.0"?>\n"""
        self._xml = xml_tag + self._xml

    def _clean_xml(self) -> None:
        self._xml = parseString(self._xml).toprettyxml()

    def write_file(self, destination_folder: Path) -> None:
        with open(destination_folder / (self.track_name+'.world'), 'w') as file:
            file.write(self._xml)


if __name__ == '__main__':
    tp = TrackParser('skidpad', add_ground=True, add_sun=True)
    tp.write_file(destination_folder=Path(__file__).parent/'data'/tp.track_name)
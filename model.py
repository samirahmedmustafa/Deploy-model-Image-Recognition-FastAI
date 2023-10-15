#!/usr/local/bin/python
import pickle
import pathlib
from pathlib import Path
import torch
from torch.hub import load_state_dict_from_url
import os,sys

pathlib.WindowsPath = pathlib.PosixPath

__version__ = "0.1.0"

class AIModel:

    def __init__(self):
        path = Path(os.getcwd())

        try:
            self.model = torch.load(os.path.join(path, "export.pkl"), map_location="cpu", pickle_module=pickle)
        except AttributeError as e: 
            e.args = [f"Custom classes or functions exported with your `Learner` not available in namespace.\Re-declare/import before loading:\n\t{e.args[0]}"]
            raise
        self.model.dls.cpu()
        if hasattr(self.model, 'channels_last'): self.model = self.model.to_contiguous(to_fp32=True)
        elif hasattr(self.model, 'mixed_precision'): self.model = self.model.to_fp32()
        elif hasattr(self.model, 'non_native_mixed_precision'): self.model = self.model.to_non_native_fp32()

    def predict(self, img):
        label, _, conf = self.model.predict(img)
        index = self.model.dls.vocab.items.index(label)
        confidence = conf[index]
        return { "label": label, "confidence": confidence }

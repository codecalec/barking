import numpy as np

from CutFlow import Event, Cut, CutFlow


class MyEvent(Event):
    pt: float
    eta: float
    phi: float
    phi2: float

    def __init__(self, pt, eta, phi, phi2):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.phi2 = phi2

    def __repr__(self):
        return f"({self.pt}, {self.eta}, {self.phi})"


class PtCut(Cut):
    description = "Limits events with pt above 5"
    required_branches = ["pt"]

    def cut(self, event):
        return event if event.pt > 5 else None

class DeltaPhiCut(Cut):
    description = "Limits events to phi between 1 and 3"
    required_branches = ["phi", "phi2"]

    def cut(self, event):
        d_phi = event.phi - event.phi2
        return event if 1 <= d_phi <= 3 else None

def make_toy_events():
    kinematics = np.random.random((10, 3)) * 10
    events = [MyEvent(*k) for k in kinematics]
    return events


if __name__ == "__main__":
    cuts = [
        PtCut(),
        DeltaPhiCut()
    ]
    cutflow = CutFlow(cuts)

    events = make_toy_events()
    print(events)
    print(len(events))

    cut_events = list(filter(cutflow.apply, events))
    print(cut_events)
    print(len(cut_events))

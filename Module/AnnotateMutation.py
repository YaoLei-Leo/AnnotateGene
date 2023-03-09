# To annotate the mutation into the plot.
import matplotlib.patches as patches

# Functions
def AnnotateSNVMutation(Axes, Position, Label, Color):
    Axes.vlines(Position, Axes.get_ylim()[0], -0.5, color=Color, alpha=0.5)
    Axes.text(Position, -0.5, s=Label, ha='center', fontsize="large", color=Color)
    
    return Axes

def AnnotateCNVMutation(Axes, Start, End, Label, Color):
    if Start>End:
        n=End
        End=Start
        Start=n
    ExonRectangle = patches.Rectangle((Start, Axes.get_ylim()[0]+0.3), End-Start, abs(Axes.get_ylim()[0])-0.85, facecolor=Color, alpha=0.5)
    Axes.add_patch(ExonRectangle)
    Axes.text((Start+(End-Start)/2), -0.5, s=Label, ha='center', fontsize="large", color=Color)
    return Axes
# To annotate the mutation into the plot.
import matplotlib.patches as patches

# Functions
def AnnotateSNVMutation(Axes, Position, Label, LabelY, Color):
    # print(Axes.get_ylim())
    # print(round(Axes.get_ylim()[0]))
    Axes.vlines(Position, round(Axes.get_ylim()[0]), -0.5, color=Color, linewidth=0.3, linestyles="solid", alpha=1)
    Axes.text(Position, LabelY, s=Label, ha='left', fontsize=6, color=Color)
    
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
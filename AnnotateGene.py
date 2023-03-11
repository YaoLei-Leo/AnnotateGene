# Main function of AnnotateGene
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from pathlib import Path
from Module import PlotGene, AnnotateMutation

def main(GenomeAssembly, GenomicRegion, Color, Figsize, DotPerInch, Mutation, MutationFile, Output):
    ScriptDir = Path( __file__ ).parent.absolute()
    ## Parse arguments to parameters
    Chr=GenomicRegion.split(':')[0]
    PosRange=GenomicRegion.split(":")[1]
    
    ax = PlotGene.PlotGene(ScriptDir, GenomeAssembly, GenomicRegion, Color, Figsize, DotPerInch)
    # ax = AnnotateMutation.AnnotateSNVMutation(ax, 179623894, "NP_001254479.2:p.(Lys3374*)", "Red")
    if Mutation:
        if Mutation.split(",")[0]=="SNV":
            ax = AnnotateMutation.AnnotateSNVMutation(ax, int(Mutation.split(",")[1]), Mutation.split(",")[2], Mutation.split(",")[3])
            # print(Mutation.split("|"))
        elif Mutation.split(",")[0]=="CNV":
            # print(Mutation.split("|"))
            ax = AnnotateMutation.AnnotateCNVMutation(ax, int(Mutation.split(",")[1]), int(Mutation.split(",")[2]), Mutation.split(",")[3], Mutation.split(",")[4])
    
    if MutationFile:
        with open(MutationFile) as f:
            y=-0.5
            for line1 in f:
                line1 = line1.strip("\n")
                list1 = line1.split(",")
                if list1[0]=="SNV":
                    ax = AnnotateMutation.AnnotateSNVMutation(ax, int(list1[1]), list1[2], y, list1[3])
                    # print(list1)
                elif list1[0]=="CNV":
                    ax = AnnotateMutation.AnnotateCNVMutation(ax, int(list1[1]), int(list1[2]), list1[3], list1[4])
                    # print(list1)
                y+=0.1
    
    ax.ticklabel_format(useOffset=False, style='plain') ## Fort axis tick label to not use scientific notaion
    tick_spacing = round((int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/30, -3) ### Add tick density, round to nearest 1000
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing)) ### Add tick density
    ax.get_yaxis().set_visible(False) ### Hide y axis
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_visible(False) ### Set left, right, and top frame
    ax.set_xlabel(Chr, fontsize=10) ### Set x label
    plt.xticks(rotation = 45, fontsize=6) ### Rotate tick angle
    plt.tight_layout() ### tight_layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area. 
    
    plt.savefig(Output, bbox_inches='tight', transparent=True)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-ga", "--GenomeAssembly", metavar="GRCh37,GRCh38", type=str, required=False, default="GRCh37", help='The genome assembly version to be used, default is GRCh37.')
    parser.add_argument("-gr", "--GenomicRegion", metavar="chr:start-end", type=str, required=True, help='The genomic region enquired. For example: chr2:179390716-179672150.')
    parser.add_argument('-c', '--Color', metavar="", type=str, required=False, default="#003c4b,#be5629,#056faf,#003c4b", help='The color of intron, UTR, exon, and transcript name, respectively. Default is "#003c4b,#be5629,#056faf,#003c4b". Hexadecimal color codes are supported.')
    parser.add_argument('-fs', '--Figsize', metavar="width,height", type=str, required=False, default="16,4", help='The size of figure use want to output. Default is "16,4".')
    parser.add_argument('-dpi', '--DotPerInch', metavar="", type=int, required=False, default=500, help='The dpi of the figure. default is 500.')
    parser.add_argument('-o', '--Output', metavar="", type=str, default="./AnnotateGene.png", required=False, help='The output image, default is "./AnnotateGene.png".')
    parser.add_argument('-m', '--Mutation', metavar="", type=str, required=False, help='The mutation user want to annotate into the figure. Input is "mutation type,position,label,color". Recommend use quotation mark here if the label contains strange symbol. (1) SNV example: "SNV,179623894,NP_001254479.2:p.(Lys3374*),Red" (2) CNV example: "CNV,179520894,179529894,1CNdeletion,Green"')
    parser.add_argument('-mf', '--MutationFile', metavar="", type=str, required=False, help='The file that contains mutations user want to annotate into the figure. Each line one mutation. Same format with a single mutation.')
    args = parser.parse_args()
    main(args.GenomeAssembly, args.GenomicRegion, args.Color, args.Figsize, args.DotPerInch, args.Mutation, args.MutationFile, args.Output)
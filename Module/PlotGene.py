# To plot the gene
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches

## Functions
def ChrToRefSeqAccn(ScriptDir, InputChr): ### Convert the "Chr2" to RefSeq accession number.
    s=0
    with open("{}/ResourceFile/GRCh37_latest_assembly_report.txt".format(ScriptDir)) as f:
        for line1 in f:
            if not line1.startswith('#'):
                list1 = line1.split()
                # print(list1)
                RefSeqAccn = list1[6]
                Chr = list1[-1]
                if InputChr == Chr:
                    s=1
                    return RefSeqAccn
        if s==0:
            raise Exception("Sorry, no corresponding RefSeq accession number found for inputted chromosome.")

def TestPosInRange(InputPos, Range):
    if int(InputPos)>=int(Range.split('-')[0]) and int(InputPos)<=int(Range.split('-')[1]):
        return True
    else:
        return False

def OrderGroupedDfByNumberOfRows(InputGroupedDf): ## To order the grouped df by the number of rows in each group. The return is a dict.
    GroupedDf_NameToLength_dict = dict()
    GroupedDf_NameToGroup_dict = dict()
    for name, group in InputGroupedDf:
        # print(group)
        # print(name)
        GroupedDf_NameToLength_dict[name]=len(group)
        GroupedDf_NameToGroup_dict[name]=group
    # print(dict(sorted(GroupedEnquiredDf_NameToLength_dict.items(), key=lambda x:x[1], reverse=True)))
    SortedGroupedDfName=dict(sorted(GroupedDf_NameToLength_dict.items(), key=lambda x:x[1], reverse=True))
    SortedGroupedDfGroup_dict = {k : GroupedDf_NameToGroup_dict[k] for k in SortedGroupedDfName}
    return SortedGroupedDfGroup_dict

def TestRangeOverlapWithRangeList(InputRange, RangeList):
    n=0
    for Range in RangeList:
        if InputRange.split("-")[1]<Range.split("-")[0] or InputRange.split("-")[0]>Range.split("-")[1]:
            continue
        else:
            n=1
            return True
    if n==0:
        return False

def PlotGene(ScriptDir, GenomeAssembly, GenomicRegion, Color, Figsize, DotPerInch, InvertXaxis):
    ### 1.Parse arguments to parameters
    RefSeqGenomicGtf="{}/ResourceFile/{}_latest_genomic.sorted.gtf.gz".format(ScriptDir, GenomeAssembly)
    Chr=GenomicRegion.split(':')[0]
    PosRange=GenomicRegion.split(":")[1]
    
    ### 2.Extract the enquired region.
    bashCommand = "tabix {} {}".format(RefSeqGenomicGtf, "{}:{}".format(ChrToRefSeqAccn(ScriptDir, Chr), PosRange))
    # print(bashCommand)
    EnquiredDf=pd.DataFrame(columns=['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute'])
    a = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    for line in a.stdout:
        line_list = line.decode(encoding='utf-8').split("\t")
        # print(line_list)
        EnquiredDf.loc[len(EnquiredDf)] = line_list
    a.wait()
                    
    ### 3.Extract gene ID and transcript ID to dataframe columns.
    EnquiredDf["geneID"] = ""
    EnquiredDf["transcriptID"] = ""
    for index,row in EnquiredDf.iterrows():
        AttributeList = row['attribute'].strip("; ").split("; ")
        GeneID = AttributeList[0].replace("\"","").split(" ")[1]
        TranscriptID = AttributeList[1].replace("\"","").split(" ")[1]
        EnquiredDf.loc[index, 'geneID'] = GeneID
        EnquiredDf.loc[index, 'transcriptID'] = TranscriptID

    GroupedEnquiredDf = EnquiredDf[EnquiredDf['feature']!='gene'].groupby("transcriptID")    

    ### 4.Sort GroupedEnquiredDf by length of dataframe.
    SortedGroupedEnquiredDfGroup = OrderGroupedDfByNumberOfRows(GroupedEnquiredDf) ### Sort grouped df by number of rows of each group.

    ### 5.Assign y value for each transcript.
    ExistTranscriptRange_dict=dict()
    MinimumY=-1
    for name in SortedGroupedEnquiredDfGroup:
        group=SortedGroupedEnquiredDfGroup[name]
        group['y']=None
        for index, row in group.iterrows():
            Feature=row["feature"]
            if Feature=="transcript":
                Start=int(row["start"])
                End=int(row["end"])
                if Start<End:
                    Range="{}-{}".format(Start, End)
                else:
                    Range="{}-{}".format(End, Start)
                
                if len(ExistTranscriptRange_dict)==0:
                    group["y"]=-1
                    ExistTranscriptRange_dict[-1]=[Range]
                else:
                    status=0
                    for key in ExistTranscriptRange_dict:
                        if TestRangeOverlapWithRangeList(Range, ExistTranscriptRange_dict[key]):
                            continue
                        else:
                            group["y"]=key
                            status=1
                            ExistTranscriptRange_dict[key].append(Range)
                            break
                    if status==0:
                        group["y"]=key-0.7
                        ExistTranscriptRange_dict[key-0.7]=[Range]
                        if key-0.7<MinimumY:
                            MinimumY=key-0.7

    ### 6.Plot the transcripts to the axes.
    fig,ax=plt.subplots(figsize=(float(Figsize.split(",")[0]),float(Figsize.split(",")[1])), dpi=int(DotPerInch))
    plt.plot()
    for name in SortedGroupedEnquiredDfGroup:
        group = SortedGroupedEnquiredDfGroup[name]
        # print(group)
        # print(name)
        for index,row in group.iterrows():
            Feature=row["feature"]
            Strand=row["strand"]
            Start=int(row["start"])
            End=int(row["end"])
            y=row["y"]
            if Feature=="transcript":
                # print(1)
                ax.hlines(y, Start, End, linestyles='solid', colors=Color.split(",")[0], zorder=1)
                if InvertXaxis==True:
                    ax.text(End, y+0.15, s=name, ha='right', color=Color.split(",")[3], fontsize=6)
                else:
                    ax.text(Start, y+0.15, s=name, ha='right', color=Color.split(",")[3], fontsize=6)
            elif Feature=="exon":
                ExonRectangle = patches.Rectangle((Start, y-0.125), End-Start, height=0.25, facecolor=Color.split(",")[1], zorder=2)
                ax.add_patch(ExonRectangle)
            elif Feature=="CDS":
                CdsRectangle = patches.Rectangle((Start, y-0.25), End-Start, height=0.5, facecolor=Color.split(",")[2], zorder=3)
                ax.add_patch(CdsRectangle)
            # elif Feature=="start_codon" or Feature=="stop_codon":
            #     CodonRectangle = patches.Rectangle((Start, y-0.25), End-Start, height=0.7, facecolor='orange', zorder=4)
            #     ax.add_patch(CodonRectangle)

    ### 7.Add transcription direction to the plot.
    for name in SortedGroupedEnquiredDfGroup:
        group = SortedGroupedEnquiredDfGroup[name]
        # print(group)
        # print(name)
        PreviousEnd="NA"
        for index,row in group.iterrows():
            Feature=row["feature"]
            Strand=row["strand"]
            Start=int(row["start"])
            End=int(row["end"])
            y=row["y"]
            if Feature=="exon":
                if PreviousEnd!="NA":
                    n=PreviousEnd+(Start-PreviousEnd)/2
                    # ax.vlines(n, y, y-0.25, color='black')
                    if abs(Start-PreviousEnd)>(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/100:
                    #     ax.vlines(n, y, y+0.25, color='Red')
                        if Strand=="+":
                            ax.plot([n+(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600, n-(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600], [y, y+(0-MinimumY)/100], color=Color.split(",")[0])
                            ax.plot([n+(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600, n-(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600], [y, y-(0-MinimumY)/100], color=Color.split(",")[0])
                        elif Strand=="-":
                            ax.plot([n-(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600, n+(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600], [y, y+(0-MinimumY)/100], color=Color.split(",")[0])
                            ax.plot([n-(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600, n+(int(PosRange.split("-")[1])-int(PosRange.split("-")[0]))/600], [y, y-(0-MinimumY)/100], color=Color.split(",")[0])
                PreviousEnd=End
                
    return ax
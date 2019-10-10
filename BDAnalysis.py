import ROOT as R
R.gROOT.SetBatch(1)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')
parser.add_argument('--output',dest='output')
args = parser.parse_args()

f=R.TFile(args.input)

import os
runID=os.path.splitext(os.path.basename(args.input))[0]

print runID

ivH_1=f.Get("ivH_1")
npoints=ivH_1.GetEntries()
g=R.TGraphErrors(int(npoints))
igood=0
xmin=999
xmax=-1
for i in range(1,ivH_1.GetNbinsX()+1):
    if (ivH_1.GetBinContent(i)>0):
        if (ivH_1.GetXaxis().GetBinCenter(i)<xmin):
            xmin=ivH_1.GetXaxis().GetBinCenter(i)
        if (ivH_1.GetXaxis().GetBinCenter(i)>xmax):
            xmax=ivH_1.GetXaxis().GetBinCenter(i)
#        print i,ivH_1.GetXaxis().GetBinCenter(i),ivH_1.GetBinContent(i),ivH_1.GetBinError(i)
        g.SetPoint(igood,ivH_1.GetXaxis().GetBinCenter(i),R.TMath.Log(ivH_1.GetBinContent(i)))
        g.SetPointError(igood,0.,1/ivH_1.GetBinContent(i)*ivH_1.GetBinError(i))
        igood+=1


fBD=R.TF1("fBD","[0]*(x-[1])*(1+[2]*(x-[1]))",xmin,xmax)
fBD.SetParameter(1,(xmax+xmin)/2.)
fBD.SetParameter(2,0.)
fBD.SetParLimits(2,0,0.1)
fBD.SetParLimits(0,0,1.E6)
fBD.SetParLimits(1,xmin,xmax)

c1=R.TCanvas("c1","c1",800,600)
for i in range(0,int(npoints)):
    ivH_1.Fit(fBD,"QB","",xmin+i*ivH_1.GetXaxis().GetBinWidth(1)+ivH_1.GetXaxis().GetBinWidth(1)/2.,xmax+ivH_1.GetXaxis().GetBinWidth(1)/2.)
    if (ivH_1.GetFunction("fBD").GetNDF()>0):
        if (R.TMath.Prob(ivH_1.GetFunction("fBD").GetChisquare(),ivH_1.GetFunction("fBD").GetNDF()>0.3)):
            bd=fBD.GetParameter(1)
            break

print "Breakdown voltage from fit:%4.2f V"%bd

text=R.TLatex()
text.SetTextSize(0.04)


c1.SetLogy(1)
R.gStyle.SetOptTitle(0)
ivH_1.SetMinimum(1)
ivH_1.SetMaximum(ivH_1.GetMaximum()*5.)
ivH_1.GetXaxis().SetRangeUser(xmin,xmax)
ivH_1.Draw()
fBD.Draw("SAME")
l=R.TLine(bd,1,bd,ivH_1.GetMaximum()/5.)
l.SetLineColor(R.kRed)
l.SetLineWidth(3)
l.SetLineStyle(2)
l.Draw("SAME")
text.DrawLatexNDC(0.12,0.91,"Run: %s"%runID)
text.DrawLatexNDC(0.2,0.7,"BD = %5.3f V"%(fBD.GetParameter(1)))
c1.SaveAs(args.output+"/"+runID+"_ivfit.png")

spl3=R.TSpline3("spl",g)
g1=R.TGraphErrors(int(npoints))
igood=0
for i in range(1,ivH_1.GetNbinsX()+1):
    if (ivH_1.GetBinContent(i)>0):
        ilnd=1/spl3.Derivative(ivH_1.GetXaxis().GetBinCenter(i)) if spl3.Derivative(ivH_1.GetXaxis().GetBinCenter(i))>0 else 0
        g1.SetPoint(igood,ivH_1.GetXaxis().GetBinCenter(i),ilnd)
        g1.SetPointError(igood,0.,0.)
        igood+=1


c1.SetLogy(0)
g1.SetMarkerStyle(20)
g1.SetMarkerSize(1.2)
g1.Draw("AP")
g1.GetXaxis().SetRangeUser(bd-0.5,bd+0.5)
g1.GetXaxis().SetTitle("Bias [V]")
g1.GetYaxis().SetTitle("ILND")
g1.SetMaximum(0.5)
g1.SetMinimum(0.)
l1=R.TLine(bd,0.,bd,0.5)
l1.SetLineColor(R.kRed)
l1.SetLineWidth(3)
l1.SetLineStyle(2)
l1.Draw("SAME")
text.DrawLatexNDC(0.12,0.91,"Run: %s"%runID)
text.DrawLatexNDC(0.2,0.7,"BD = %5.3f V"%(fBD.GetParameter(1)))
c1.SaveAs(args.output+"/"+runID+"_ilnd.png")

out=R.TFile(args.output+"/"+runID+"_bdAnalysis.root","RECREATE")
ivH_1.Write()
g.Write("ILN")
spl3.Write("ILNSpline")
g1.Write("ILND")
out.Close()



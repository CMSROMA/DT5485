import ROOT as R
R.gROOT.SetBatch(1)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-i","--input")
(options,args)=parser.parse_args()

IVData=R.TTree("IVData","IVData")
IVData.ReadFile(options.input,"chStatus/I:vset/F:vout/F:iout/F:time/D")

c1 = R.TCanvas("c1","c1",800,600)
ivH=R.TH2F("ivH","ivH",300,44.45,74.45,4000,0.,2000.)
IVData.Project("ivH","iout*1000:vset","iout<10")
ivH.FitSlicesY()
ivH_1 = R.gDirectory.Get("ivH_1")
ivH_2 = R.gDirectory.Get("ivH_2")
#c1.SetLogy(1)
R.gStyle.SetOptTitle(0)

ivH_1.SetStats(0)
#ivH_1.SetMaximum(ivH_1.GetMaximum()*10)
ivH_1.GetXaxis().SetTitle("Bias [V]")
ivH_1.GetYaxis().SetTitle("Current [#muA]")
ivH_1.SetMarkerStyle(20)
ivH_1.SetMarkerSize(0.8)
ivH_1.SetMarkerColor(R.kBlack)
ivH_1.SetLineColor(R.kBlack)
#ivH_1.Draw()
#c1.SaveAs("IV.png")

#findBD(ivH_1)
#c1.SaveAs("IVfit.png")

c1.SetLogy(0)
R.gStyle.SetOptStat(0)
R.gStyle.SetOptFit(111)
#ivH_2.SetStats(0)
ivH_2.GetXaxis().SetTitle("Bias [V]")
ivH_2.GetYaxis().SetTitle("#sigma_{I} [#muA]")
ivH_2.SetMarkerStyle(20)
ivH_2.SetMarkerSize(0.8)
ivH_2.SetMarkerColor(R.kBlack)
ivH_2.SetLineColor(R.kBlack)
#ivH_2.Draw()
#ivH_2.Fit("pol0")
#c1.SaveAs("IV_noise.png")

print "Writing output to "+options.input.replace(".csv",".root")
f=R.TFile(options.input.replace(".csv",".root"),"RECREATE")
IVData.Write()
ivH.Write()
ivH_1.Write()
ivH_2.Write()
f.Close()

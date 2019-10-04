import ROOT as R
R.gROOT.SetBatch(1)

def findBD(iv):
    max_step0=-1
    min_step1=-1
    minimum=45.5
    step=0
    pars={}
    for i in range(0,20):
        if (step==0):
            print("Step0")
            iv.Fit("expo","R","",minimum,48.5+i)
        elif (step==1):
            if (minimum>60):
                break
            iv.Fit("expo","R","",minimum,70.5)
            minimum+=1
        if (iv.GetFunction("expo").GetNDF()>0):
            chi2=iv.GetFunction("expo").GetChisquare()/iv.GetFunction("expo").GetNDF()
            print(chi2)
            if (chi2>3 and i>2 and step==0):
                max_step0=48.5+i-1
                minimum=48.5+i
                step=1
                print("Max step0 found %5.3f"%max_step0)
                continue
            if (chi2<100 and step==1): #to be fixed later
                min_step1=minimum-1
                print("Min step1 found %5.3f"%min_step1)
                break
    if (max_step0>0 and min_step1>0):      

        iv.Fit("expo","QR","",45.5,max_step0)
        pars['step0']=[]
        pars['step0'].append(iv.GetFunction("expo").GetParameter(0))
        pars['step0'].append(iv.GetFunction("expo").GetParameter(1))

        f0=R.TF1("f0","expo",45,70)
        f0.SetParameter(0,pars['step0'][0])
        f0.SetParameter(1,pars['step0'][1])
        f0.SetLineColor(R.kBlack)
        f0.SetLineWidth(2)
        f0.Draw("SAME")
  
        iv.Fit("expo","QR","",min_step1,70)
        pars['step1']=[]
        pars['step1'].append(iv.GetFunction("expo").GetParameter(0))
        pars['step1'].append(iv.GetFunction("expo").GetParameter(1))

        bd=(pars['step1'][0]-pars['step0'][0])/(pars['step0'][1]-pars['step1'][1])
        print("BD=%4.2f"%bd)



IVData=R.TTree("IVData","IVData")
IVData.ReadFile("ivscan.csv","vset/F:vout/F:iout/F")

c1 = R.TCanvas("c1","c1",800,600)
ivH=R.TH2F("ivH","ivH",100,44.5,54.5,200,0.,50.)
IVData.Project("ivH","iout*1000:vout","iout<0.05")
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
ivH_1.Draw()
c1.SaveAs("IV.png")

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
ivH_2.Draw()
ivH_2.Fit("pol0")
c1.SaveAs("IV_noise.png")

f=R.TFile("ivscan.root","RECREATE")
IVData.Write()
ivH.Write()
ivH_1.Write()
ivH_2.Write()
f.Close()

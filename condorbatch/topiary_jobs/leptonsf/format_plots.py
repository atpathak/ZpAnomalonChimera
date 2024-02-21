import ROOT

def sethistParmas(hist):
    hist.SetStats(0)
    hist.GetYaxis().SetTitle("p_{T}")
    hist.GetYaxis().SetTitleOffset(1)

def settcanvasParmas(can):
    can.SetBottomMargin(0.15)
    can.SetRightMargin(0.2)
    can.SetLeftMargin(0.15)

if __name__=='__main__':

    f = ROOT.TFile("NUM_Mu50_TkMu50_DEN_TightID_abseta_pt_2016.root")    
    hsf = f.Get("NUM_Mu50_TkMu50_DEN_TightID_abseta_pt")
    #hdeff = f.Get("NUM_Mu50_TkMu50_DEN_TightID_abseta_pt_efficiencyData")
    #hmceff = f.Get("NUM_Mu50_TkMu50_DEN_TightID_abseta_pt_efficiencyMC")

    histlist = [hsf]#,hdeff,hmceff]
    fnames = ["2016_muon_trigger_sf_Mu50_TkMu50_DEN_TightID_abseta_pt.pdf",
              "2016_muon_trigger_dataeff_Mu50_TkMu50_DEN_TightID_abseta_pt.pdf",
              "2016_muon_trigger_mceff_Mu50_TkMu50_DEN_TightID_abseta_pt.pdf"]
    titles = ["TightID muon p_{T} > 20 , Mu50 OR TkMu50 SF 2016"]
              #"TightID muon p_{T} > 60, Mu55 OR Mu100 OR TkMu100 Data 2016",
              #"TightID muon p_{T} > 60, Mu55 OR Mu100 OR TkMu100 MC 2016"]

    for h,hist in enumerate(histlist):
        hist.SetTitle(titles[h])
        sethistParmas(hist)
    
        tc1 = ROOT.TCanvas("tc1","tc1",600,400)
        settcanvasParmas(tc1)
        hist.Draw("colz")
    
        tc1.SaveAs(fnames[h])

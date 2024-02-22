import ROOT

tf = ROOT.TFile("DeepAK8MassDecorrelZHbbvQCD_ttscalefactors_Zptcut_Hptcut_metcut_btagwp.root","r")

keys = tf.GetListOfKeys()

for key in keys:
    name = key.GetName()
    if "unc" in name:
        continue
    h = tf.Get(name)

    tc = ROOT.TCanvas("tc","tc",800,600)
    tc.cd()

    h.GetXaxis().SetTitle("p_{T}")
    h.GetYaxis().SetTitle("tt btag Scale Factor")
    h.SetTitle(name.split("sf")[0])
    h.SetStats(0)
    h.Draw()

    tc.SaveAs(name+"_tt.png")

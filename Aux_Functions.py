import ROOT
import math

#--------------Atlas Style---------------------------------------------------
class AtlasStyle( ROOT.TStyle ):

    ##
    # @short Object constructor
    #
    # The constructor just initializes the underlying TStyle object, and
    # calls the configure() function to set up the ATLAS style.
    #
    # The parameters of the constructor should just be ignored in 99.9%
    # of the cases.
    #
    # @param name The name given to the style
    # @param title The title given to the style
    def __init__( self, name = "AtlasStyle", title = "ATLAS style object" ):

        # Initialise the base class:
        ROOT.TStyle.__init__( self, name, title )
        self.SetName( name )
        self.SetTitle( title )

        # Call the configure function for setting up the style:
        self.configure()

        return

    ##
    # @short Configure the object for the ATLAS style
    #
    # This function actually takes care of setting up the ATLAS style.
    # I implemented it based on a C++ TStyle object, which in turn was
    # implemented based on a central piece of CINT macro.
    def configure( self ):

        # Tell the user what we're doing:
        self.Info( "configure", "Configuring default ATLAS style" )

        # Use plain black on white colors:
        icol = 0
        self.SetFrameBorderMode( 0 )
        self.SetFrameFillColor( icol )
        self.SetFrameFillStyle( 0 )
        self.SetCanvasBorderMode( 0 )
        self.SetPadBorderMode( 0 )
        self.SetPadColor( icol )
        self.SetCanvasColor( icol )
        self.SetStatColor( icol )

        # Set the paper and margin sizes:
        self.SetPaperSize( 20, 26 )
        self.SetPadTopMargin( 0.10 )		#0.05
        self.SetPadRightMargin( 0.025 )		#0.05
        self.SetPadBottomMargin( 0.10 )		#0.16
        self.SetPadLeftMargin( 0.12 )		#0.16

        # set title offsets (for axis label)
        self.SetTitleXOffset(1.3);			#1.4
        self.SetTitleYOffset(1.3);			#1.4
		#self.SetTitleOffset(0.5);

        # Use large fonts:
        font_type = 42
        font_size = 0.04
        self.SetTextFont( font_type )
        self.SetTextSize( font_size )
        self.SetLabelFont( font_type, "x" )
        self.SetLabelSize( font_size, "x" )
        self.SetTitleFont( font_type, "x" )
        self.SetTitleSize( font_size, "x" )
        self.SetLabelFont( font_type, "y" )
        self.SetLabelSize( font_size, "y" )
        self.SetTitleFont( font_type, "y" )
        self.SetTitleSize( font_size, "y" )
        self.SetLabelFont( font_type, "z" )
        self.SetLabelSize( font_size, "z" )
        self.SetTitleFont( font_type, "z" )
        self.SetTitleSize( font_size, "z" )

        # Use bold lines and markers:
        #self.SetMarkerStyle( 20 )
        #self.SetMarkerSize( 1.2 )
        #self.SetHistLineWidth( 2 )
        #self.SetLineStyleString( 2, "[12 12]" )

        # Do not display any of the standard histogram decorations:
        self.SetOptTitle( 0 )
        self.SetOptStat( 0 )
        self.SetOptFit( 0 )

        # Put tick marks on top and rhs of the plots:
        self.SetPadTickX( 1 )
        self.SetPadTickY( 1 )

        return

#--------------Create_Hists.py-----------------------------------------------
def MakeLegend(h1,h2):
	leg = ROOT.TLegend(0.2,0.77,0.5,0.87)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.SetTextSize(0.04)
	#leg.AddEntry(h1,"min_n_tchannels (signal)","f")
	#leg.AddEntry(h2,"W+jets","f")
	leg.AddEntry(h1,"min_n_tchannels (signal)","l")
	leg.AddEntry(h2,"W+jets","l")
	return leg
	
def SetHistStyle(h1,h2,max_1,max_2,min_1,min_2):
	#h1.SetFillColor(ROOT.TAttFill.kYellow)
	#h1.SetLineColor(ROOT.TAttLine.kBlack)
	h1.SetLineColor(ROOT.TAttLine.kBlue)
	h1.SetLineWidth(3)
	h1.GetYaxis().SetTitleOffset(1.5)
	#h2.SetFillColor(ROOT.TAttFill.kGreen-8)
	#h2.SetLineColor(ROOT.TAttLine.kBlack)
	h2.SetLineColor(ROOT.TAttLine.kRed)
	h2.SetLineWidth(3)
	h2.GetYaxis().SetTitleOffset(1.5)
	if max_1 > max_2 and max_1 != 0:
		h1.SetMaximum(10*max_1)
		if min_1 < min_2:
			h1.SetMinimum(min_1/5)
		else:
			h1.SetMinimum(min_2/5)
	elif max_2 > max_1 and max_2 != 0:
		h2.SetMaximum(10*max_2)
		if min_1 < min_2:
			h2.SetMinimum(min_1/5)
		else:
			h2.SetMinimum(min_2/5)
	return h1, h2
	
#--------------Find_Error_Band.py-------------------------------------------------
def MakeErrorBandLegend(h1,h2):
	leg = ROOT.TLegend(0.55,0.77,0.75,0.87)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.SetTextSize(0.04)
	leg.AddEntry(h1,"Nominal Sherpa","l")
	leg.AddEntry(h2,"Systematic Error","f")
	return leg
	
def FindErrorBands(datasets,root_file,hist):
	rebin = 4					# Set this to how many bins should be merged (1 -> no change)
	nom_hist = root_file.Get(datasets[0]+"/Normalized/"+hist+'_norm')
	nom_hist = nom_hist.Clone()
	nom_hist.Rebin(rebin)
	nom_graph = ROOT.TGraphAsymmErrors(nom_hist)
	nom_graph.SetLineColor(ROOT.TAttFill.kGreen)
	nbins = nom_hist.GetNbinsX()

	upper_error = []
	lower_error = []
	sequence = datasets[1:]
	for bin in range(1,nbins+1):
		positive_shifts2 = []
		negative_shifts2 = []
		nom_bin_val = nom_hist.GetBinContent(bin)
		nom_bin_err = nom_hist.GetBinError(bin)

		for dataset in sequence:
			hist_to_clone = root_file.Get(dataset+"/Normalized/"+hist+'_norm')
			hist_to_comp = hist_to_clone.Clone(dataset)
			hist_to_comp.Rebin(rebin)

			comp_bin_val = hist_to_comp.GetBinContent(bin)
			comp_bin_err = hist_to_comp.GetBinError(bin)

			diff = comp_bin_val - nom_bin_val
			if diff > 0.0:
				positive_shifts2.append(diff*diff)
			else:
				negative_shifts2.append(diff*diff)

		upper_error.append(math.sqrt(math.fsum(positive_shifts2)))
		lower_error.append(math.sqrt(math.fsum(negative_shifts2)))

		nom_graph.SetPointEYhigh(bin-1,upper_error[bin-1])
		nom_graph.SetPointEYlow(bin-1,lower_error[bin-1])

	return nom_hist, nom_graph
	
def MakeRatioPlot(nom_hist,nom_graph):
	npoints = nom_hist.GetNbinsX()
	ratio_plot = ROOT.TGraphAsymmErrors(npoints)
	for point in range(npoints):
		Error_High = nom_graph.GetErrorYhigh(point)
		Error_Low = nom_graph.GetErrorYlow(point)
		Y_point = nom_hist.GetBinContent(point+1)
		X_point = nom_hist.GetBinCenter(point+1)
		X_Axis = nom_hist.GetXaxis()
		ratio_up = Error_High/Y_point
		ratio_down = Error_Low/Y_point
		print X_point, ratio_up, ratio_down
		ratio_plot.SetPoint(point, X_point, 1.0)
		ratio_plot.SetPointEXhigh(point, nom_hist.GetBinWidth(point)/2.0)
		ratio_plot.SetPointEXlow(point, nom_hist.GetBinWidth(point)/2.0)
		ratio_plot.SetPointEYhigh(point, ratio_up)
		ratio_plot.SetPointEYlow(point, ratio_down)

	return ratio_plot

#-----------Used by all---------------------------------------------------------
def GetListDataset(list_name):
	# This function returns the list that is associated with the string 'list_name'.
	# i.e., GetListDataset('datasets') returns the list datasets
	# Names of new lists must be put in the list_of_lists list.
	
	datasets = 	['mc12_8TeV.129916.Sherpa_CT10_Wmunu2JetsEW1JetQCD15GeV_min_n_tchannels.evgen.EVNT.e1557/',
				 'mc12_8TeV.147294.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30.evgen.EVNT.e1805/',
				 'mc12_8TeV.147295.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_CKKW30_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147296.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown.evgen.EVNT.e1805/',
				 'mc12_8TeV.147297.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFdown_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147298.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup.evgen.EVNT.e1805/',
				 'mc12_8TeV.147299.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuFup_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147300.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1.evgen.EVNT.e1805/',
				 'mc12_8TeV.147301.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi1_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147302.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2.evgen.EVNT.e1805/',
				 'mc12_8TeV.147303.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_mpi2_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147304.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1.evgen.EVNT.e1805/',
				 'mc12_8TeV.147305.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_Shower1_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147306.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown.evgen.EVNT.e1805/',
				 'mc12_8TeV.147307.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRdown_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147308.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup.evgen.EVNT.e1805/',
				 'mc12_8TeV.147309.Sherpa_CT10_EWK_Wmunu_min_n_tchannels_MuRup_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147310.Sherpa_CT10_Wmunu_CKKW30.evgen.EVNT.e1805/',
				 'mc12_8TeV.147311.Sherpa_CT10_Wmunu_CKKW30_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147312.Sherpa_CT10_Wmunu_MuFdown.evgen.EVNT.e1805/',
				 'mc12_8TeV.147313.Sherpa_CT10_Wmunu_MuFdown_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147314.Sherpa_CT10_Wmunu_MuFup.evgen.EVNT.e1805/',
				 'mc12_8TeV.147315.Sherpa_CT10_Wmunu_MuFup_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147316.Sherpa_CT10_Wmunu_mpi1.evgen.EVNT.e1805/',
				 'mc12_8TeV.147317.Sherpa_CT10_Wmunu_mpi1_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147318.Sherpa_CT10_Wmunu_mpi2.evgen.EVNT.e1805/',
				 'mc12_8TeV.147319.Sherpa_CT10_Wmunu_mpi2_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147320.Sherpa_CT10_Wmunu_Shower1.evgen.EVNT.e1805/',
				 'mc12_8TeV.147321.Sherpa_CT10_Wmunu_Shower1_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147322.Sherpa_CT10_Wmunu_MuRdown.evgen.EVNT.e1805/',
				 'mc12_8TeV.147323.Sherpa_CT10_Wmunu_MuRdown_MjjFilt.evgen.EVNT.e1805/',
				 'mc12_8TeV.147324.Sherpa_CT10_Wmunu_MuRup.evgen.EVNT.e1805/',
				 'mc12_8TeV.147325.Sherpa_CT10_Wmunu_MuRup_MjjFilt.evgen.EVNT.e1805/']

	dataset_names = ["129916.Nominal_Sherpa_Signal", "147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
					"147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
					"147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
					"147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
					"147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
					"147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
					"147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
					"147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt",
					"147310.CKKW30", "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
					"147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
					"147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
					"147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt"]
				
	dataset_names_1 = ["147294.min_n_tchannels_CKKW30", "147295.min_n_tchannels_CKKW30_MjjFilt",
					"147296.min_n_tchannels_MuFdown", "147297.min_n_tchannels_MuFdown_MjjFilt",
					"147298.min_n_tchannels_MuFup", "147299.min_n_tchannels_MuFup_MjjFilt",
					"147300.min_n_tchannels_mpi1", "147301.min_n_tchannels_mpi1_MjjFilt",
					"147302.min_n_tchannels_mpi2", "147303.min_n_tchannels_mpi2_MjjFilt",
					"147304.min_n_tchannels_Shower1", "147305.min_n_tchannels_Shower1_MjjFilt",
					"147306.min_n_tchannels_MuRdown", "147307.min_n_tchannels_MuRdown_MjjFilt",
					"147308.min_n_tchannels_MuRup", "147309.min_n_tchannels_MuRup_MjjFilt"]

	dataset_names_2 = ["147310.CKKW30", "147311.CKKW30_MjjFilt", "147312.MuFdown", "147313.MuFdown_MjjFilt",
					"147314.MuFup", "147315.MuFup_MjjFilt", "147316.mpi1", "147317.mpi1_MjjFilt",
					"147318.mpi2", "147319.mpi2_MjjFilt", "147320.Shower1", "147321.Shower1_MjjFilt",
					"147322.MuRdown", "147323.MuRdown_MjjFilt", "147324.MuRup", "147325.MuRup_MjjFilt"]
				
	datasets_sig = 	["129916.Nominal_Sherpa_Signal", "147294.min_n_tchannels_CKKW30","147296.min_n_tchannels_MuFdown",
					"147300.min_n_tchannels_mpi1","147302.min_n_tchannels_mpi2","147304.min_n_tchannels_Shower1",
					"147306.min_n_tchannels_MuRdown","147308.min_n_tchannels_MuRup"]

	datasets_back = ["129916.Nominal_Sherpa_Background", "147310.CKKW30", "147312.MuFdown", "147314.MuFup", 
					"147316.mpi1",	"147318.mpi2", "147320.Shower1", "147322.MuRdown", "147324.MuRup"]
				
	exp_hist_list = ["d01-x01-y01", "d01-x01-y02", "d02-x01-y01", "d02-x01-y02",
				"d03-x01-y01", "d03-x01-y02", "d04-x01-y01", "d04-x01-y02",
				"d05-x01-y01", "d05-x01-y02", "d06-x01-y01", "d06-x01-y02",
				"d07-x01-y01", "d07-x01-y02", "d08-x01-y01", "d08-x01-y02",
				"d09-x01-y01", "d09-x01-y02", "d10-x01-y01", "d10-x01-y02",
				"d11-x01-y01", "d11-x01-y02", "d12-x01-y01", "d12-x01-y02",
				"d13-x01-y01", "d13-x01-y02", "d14-x01-y01", "d14-x01-y02",
				"d15-x01-y01", "d15-x01-y02", "d16-x01-y01", "d16-x01-y02",
				"d17-x01-y01", "d17-x01-y02", "d18-x01-y01", "d18-x01-y02",
				"d19-x01-y01", "d19-x01-y02", "d20-x01-y01", "d20-x01-y02",
				"d21-x01-y01", "d21-x01-y02", "d22-x01-y01", "d22-x01-y02",
				"d23-x01-y01", "d23-x01-y02", "d24-x01-y01", "d24-x01-y02",
				"d25-x01-y01", "d25-x01-y02"]
			
	hist_list = ["NJetExcl_1", "NJetExcl_2", "RatioNJetExcl_1", "RatioNJetExcl_2", "FirstJetPt_2jet_1", "FirstJetPt_2jet_2",
				"FirstJetPt_3jet_1", "FirstJetPt_3jet_2", "FirstJetPt_4jet_1", "FirstJetPt_4jet_2", "SecondJetPt_2jet_1", "SecondJetPt_2jet_2",
				"SecondJetPt_3jet_1", "SecondJetPt_3jet_2", "SecondJetPt_4jet_1", "SecondJetPt_4jet_2", "ThirdJetPt_3jet_1", "ThirdJetPt_3jet_2",
				"ThirdJetPt_4jet_1", "ThirdJetPt_4jet_2", "FourthJetPt_4jet_1", "FourthJetPt_4jet_2", "Ht_2jet_1", "Ht_2jet_2",
				"Ht_3jet_1", "Ht_3jet_2", "Ht_4jet_1", "Ht_4jet_2", "Minv_2jet_1", "Minv_2jet_2", "Minv_3jet_1", "Minv_3jet_2",
				"Minv_4jet_1", "Minv_4jet_2", "JetRapidity_1", "JetRapidity_2", "DeltaYElecJet_1", "DeltaYElecJet_2", "SumYElecJet_1", "SumYElecJet_2",
				"DeltaR_2jet_1", "DeltaR_2jet_2", "DeltaY_2jet_1", "DeltaY_2jet_2", "DeltaPhi_2jet_1", "DeltaPhi_2jet_2",
				"DijetMass_2jet_1", "DijetMass_2jet_2", "DijetMass_3jet_1", "DijetMass_3jet_2",
				"DijetMass_4jet_1", "DijetMass_4jet_2","AntiDijetMass_2jet_1", "AntiDijetMass_2jet_2",
				"AntiDijetMass_3jet_1", "AntiDijetMass_3jet_2","AntiDijetMass_4jet_1", "AntiDijetMass_4jet_2",
				"ThirdZep_3jet_1", "ThirdZep_3jet_2", "ThirdZep_4jet_1", "ThirdZep_4jet_2", "FourthZep_4jet_1", "FourthZep_4jet_2",
				"AntiDijetEtaDiff_2jet_1", "AntiDijetEtaDiff_2jet_2", "AntiDijetEtaDiff_3jet_1", "AntiDijetEtaDiff_3jet_2",
				"AntiDijetEtaDiff_4jet_1", "AntiDijetEtaDiff_4jet_2", "AntiDijetPhiDiff_2jet_1", "AntiDijetPhiDiff_2jet_2", 
				"AntiDijetPhiDiff_3jet_1", "AntiDijetPhiDiff_3jet_2", "AntiDijetPhiDiff_4jet_1", "AntiDijetPhiDiff_4jet_2"]
			
	title_list = 	["Jet Multiplicity (W+#geq 2 jets)", "Jet Multiplicity Ratio", "First Jet p_{T} (W+#geq 2 jets)", "First Jet p_{T} (W+#geq 3 jets)", "First Jet p_{T} (W+#geq 4 jets)",
					"Second Jet p_{T}", "Second Jet p_{T} (W+#geq 3 jets)", "Second Jet p_{T} (W+#geq 4 jets)", "Third Jet p_{T}", "Third Jet p_{T} (W+#geq 4 jets)",
					"Fourth Jet p_{T}", "H_{T} (W+#geq 2 jets)", "H_{T} (W+#geq 3 jets)", "H_{T} (W+#geq 4 jets)", "Jet Invariant Mass (W+ #geq 2 jets)",
					"Jet Invariant Mass (W+ #geq 3 jets)", "Jet Invariant Mass (W+ #geq 4 jets)", "First Jet Rapidity", "Lepton-Jet Rapidity Difference", "Lepton-Jet Rapidity Sum", 
					"#Delta R Distance of Leading Jets", "Rapidity Distance of Leading Jets", "Azimuthal Distance of Leading Jets","Dijet Mass (W+#geq 2 jets)",
					"Dijet Mass (W+#geq 3 jets)", "Dijet Mass (W+#geq 4 jets)", "Most Forward/Rearward Dijet Mass (W+#geq 2 jets)","Most Forward/Rearward Dijet Mass (W+#geq 3 jets)",
					"Most Forward/Rearward Dijet Mass (W+#geq 4 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 3 jets)", "Third Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)",
					"Fourth Jet Pseudorapidity in Dijet CM (W+#geq 4 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 2 jets)",
					"Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 3 jets)", "Pseudorapidity Diff b/w Most Forward-Rearward Jets (W+#geq 4 jets)",
					"cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 2 jets)", "cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 3 jets)",
					"cos|#phi_{j_1}-#phi_{j_2}| b/w Most Forward-Rearward Jets (W+#geq 4 jets)"]
				
	x_axis_list = 	["N_{jet}", "N_{jet}", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]",
					 "p_{T} [GeV]", "p_{T} [GeV]", "p_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]", "H_{T} [GeV]",
					 "m(jets) [GeV]", "m(jets) [GeV]", "m(jets) [GeV]", "y", "y(Lepton)-y(First Jet)", "y(Lepton)+y(First Jet)",
					 "#Delta R(First Jet, Second Jet)", "#Delta y(First Jet, Second Jet)", "#Delta#phi(First Jet, Second Jet)",
					 "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]", "m_{jj} [GeV]",
					 "#eta_{3} (Third Jet)", "#eta_{3} (Third Jet)", "#eta_{4} (Fourth Jet)",
					 "#Delta#eta_{j_1j_2}", "#Delta#eta_{j_1j_2}", "#Delta#eta_{j_1j_2}",
					 "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|", "cos|#phi_{j_1}-#phi_{j_2}|"]

	y_axis_list = 	["#sigma (W+#geq N_{jet} jets) [pb]", "#sigma (#geq N_{jet} jets)/#sigma (#geq N_{jet}-1 jets)",
					 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
					 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
					 "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]", "d#sigma/dp_{T} [pb/GeV]",
					 "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]", "d#sigma/dH_{T} [pb/GeV]",
					 "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]", "d#sigma/d#it{m} [pb/GeV]",
					 "d#sigma/d#it{y} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Sigma#it{y} [pb]",
					 "d#sigma/d#Delta#it{R} [pb]", "d#sigma/d#Delta#it{y} [pb]", "d#sigma/d#Delta#phi [pb]",
					 "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
					 "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]", "d#sigma/dm_{jj} [pb/GeV]",
					 "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{3} [pb]", "d#sigma/d#eta_{4} [pb]",
					 "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]", "d#sigma/d#eta_{j_1j_2} [pb]",
					 "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [pb]"]
				
	y_axis_list_norm = 	["#sigma (W+#geq N_{jet} jets)", "#sigma (#geq N_{jet} jets)/#sigma (#geq N_{jet}-1 jets)",
						 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
						 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
						 "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]", "d#sigma/dp_{T} [events/GeV]",
						 "d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]", "d#sigma/dH_{T} [events/GeV]",
						 "d#sigma/d#it{m} [events/GeV]","d#sigma/d#it{m} [events/GeV]", "d#sigma/d#it{m} [events/GeV]",
						 "d#sigma/d#it{y} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Sigma#it{y} [events]",
						 "d#sigma/d#Delta#it{R} [events]", "d#sigma/d#Delta#it{y} [events]", "d#sigma/d#Delta#phi [events]",
						 "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
						 "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]", "d#sigma/dm_{jj} [events/GeV]",
						 "d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{3} [events]", "d#sigma/d#eta_{4} [events]",
						 "d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]", "d#sigma/d#eta_{j_1j_2} [events]",
						 "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]", "d#sigma/dcos|#phi_{j_1}-#phi_{j_2}| [events]"]
					
	list_of_lists = 	['datasets', 'dataset_names', 'dataset_names_1', 'dataset_names_2', 'datasets_sig', 'datasets_back',
						'exp_hist_list', 'hist_list', 'title_list', 'x_axis_list', 'y_axis_list', 'y_axis_list_norm']
						
	if list_name in list_of_lists: return eval(list_name)
	else: return 'The given list is not defined.'

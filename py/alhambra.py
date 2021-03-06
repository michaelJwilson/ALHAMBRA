import  numpy              as  np
import  pylab              as  pl
import  pandas             as  pd
import  matplotlib         as  mpl
import  matplotlib.pyplot  as  plt

## plt.style.use('ggplot')
## mpl.rc('text', usetex = True)


if __name__ == '__main__':
  cols = ['id',    'objID', 'Field', 'Pointing', 'CCD', 'RAdeg', 'DECdeg', 'x', 'y', 'area', 'fwhm', 'stell', 'ell', 'a', 'b',\
          'theta', 'rk', 'rf', 's2n', 'photoflag', 'F365W', 'dF365W', 'F396W', 'dF396W', 'F427W', 'dF427W', 'F458W', 'dF458W',\
          'F489W', 'dF489W', 'F520W', 'dF520W', 'F551W', 'dF551W', 'F582W', 'dF582W', 'F613W', 'dF613W', 'F644W', 'dF644W', 'F675W',\
          'dF675W', 'F706W', 'dF706W', 'F737W', 'dF737W', 'F768W', 'dF768W', 'F799W', 'dF799W', 'F830W', 'dF830W', 'F861W', 'dF861W',\
          'F892W', 'dF892W', 'F923W', 'dF923W', 'F954W', 'dF954W', 'J', 'dJ', 'H', 'dH', 'KS', 'dKS', 'F814W', 'dF814W', 'F814W_3arcs',\
          'dF814W_3arcs', 'F814W_3arcs_corr', 'nfobs', 'xray', 'PercW', 'Satur_Flag', 'Stellar_Flag', 'zb_1', 'zb_min_1', 'zb_max_1', 'tb_1',\
          'Odds_1', 'Chi2', 'Stell_Mass_1', 'M_ABS_1', 'irms_OPT_Flag', 'irms_NIR_Flag', 'ra_xypx', 'dec_xypx', 'ra_aipx', 'dec_aipx', 'F814W_Image']

  keep = ['id', 'objID', 'stell', 'photoflag', 'xray', 'zb_1', 'zb_min_1', 'zb_max_1', 'tb_1', 'Odds_1', 'Chi2', 'Stell_Mass_1', 'M_ABS_1']

  '''
  ID                         ID            ID
  objID                      ID            ID
  stell                      Number        SExtractor stellarity (1 = star; 0 = galaxy)
  photoflag                  Number        SExtractor Photometric Flag
  xray                       Bool          X-Ray Source [0:NO, 1:YES] (2XMM;Watson et al. 2009;A&A493,339-373)
  zb_1                       Double        BPZ most likely redshift for the First Peak
  zb_min_1                   Double        Lower limit (95p confidence) for the First Peak
  zb_max_1                   Double        Upper limit (95p confidence) for the First Peak
  tb_1                       Integer       BPZ most likely spectral type for the First Peak
  Odds_1                     Double        P(z) contained within zb +/- 0.02 * (1 + z) for the First Peak
  Chi2                       Double        Poorness of BPZ fit: observed vs. model fluxes
  Stell_Mass_1               Double        Stellar Mass for the First Peak (log10(M_sun))
  M_ABS_1                    mags          Absolute Magnitude [AB] (B_JOHNSON) for the First Peak
  '''

  ##  data      = pd.read_csv("../dat/alhambra_light.csv", header=1, names = cols)
  data          = pd.read_csv("../dat/alhambra.csv",       header=1, names = cols)
  
  ## Viironen (1501.05109) cut on good quality photometry in all filters; "reduces sample to 8023 galaxies" 
  data          = data[data['irms_OPT_Flag'] == 0.]
  data          = data[data['irms_NIR_Flag'] == 0.]
  data          = data[data['stell']         == 0.]
  
  data          = data.ix[:, keep]
  
  (dNdz, bins)  = np.histogram(data['zb_1'], bins = np.arange(0.0, 6.0, 0.10))

  dNdz          = dNdz.astype(np.float)
  bins          = bins[:-1]

  dz            = bins[1] - bins[0]
  midz          = bins + dz/2.

  cumulative    = np.cum(dNdz)

  pl.plot(bins, cumulative, label = 'Alhambra BPZ')

  pl.xlabel(r'$z$')
  pl.ylabel(r'$N(<z)$')

  pl.savefig('../plots/dNdz.pdf')

  print data

  print('\n\nDone.\n\n')

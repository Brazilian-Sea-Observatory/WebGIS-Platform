export const TMPT_LOADER = `<div role="progressbar" aria-valuemin="0" aria-valuemax="100"
class="v-progress-circular v-progress-circular--indeterminate mercator-color--text"
style="height: 80px;width: 80px;transform: translate(50vw, 25vh);">
    <svg xmlns="http://www.w3.org/2000/svg"
        viewBox="22.857142857142858 22.857142857142858 45.714285714285715 45.714285714285715"
        style="transform: rotate(0deg);">
        <circle fill="transparent" cx="45.714285714285715" cy="45.714285714285715" r="20"
        stroke-width="5.714285714285714" stroke-dasharray="125.664" stroke-dashoffset="125.66370614359172px"
        class="v-progress-circular__overlay"></circle>
    </svg>
    <div class="v-progress-circular__info">
  </div>
</div>`;

export const TMPT_LOADER_MESSAGE = (str: string) => `<div role="progressbar" aria-valuemin="0" aria-valuemax="100"
class="v-progress-circular v-progress-circular--indeterminate mercator-color--text"
style="height: 80px;width: 80px;transform: translate(50vw, 25vh);">
    <svg xmlns="http://www.w3.org/2000/svg"
        viewBox="22.857142857142858 22.857142857142858 45.714285714285715 45.714285714285715"
        style="transform: rotate(0deg);">
        <circle fill="transparent" cx="45.714285714285715" cy="45.714285714285715" r="20"
        stroke-width="5.714285714285714" stroke-dasharray="125.664" stroke-dashoffset="125.66370614359172px"
        class="v-progress-circular__overlay"></circle>
    </svg>
    <div class="v-progress-circular__info" style="margin-top:4rem; font-weight:bold; text-align: center;">
      ${str}
    </div>
</div>`;

export const TMPT_MENU = `<button id="time-skip--play" type="button"
class="v-btn v-btn--absolute v-btn--floating v-btn--left v-btn--small theme--light mercator-color"
style="margin-left: -1.5rem;">
  <div class="v-btn__content">
    <i aria-hidden="true" class="v-icon material-icons theme--light">menu</i>
  </div>
</button>`;

export function TMPT_USERPOINT(latlng = { lat: 0, lng: 0 }, openPanelabel = 'Analisar ponto', value: number = 0) {
    return (
        `<div style="display:flex; align-items: center;">
  <img style="height: 2em; margin-right: 1rem;"` +
        // tslint:disable-next-line:max-line-length
        'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAW4AAAKACAMAAACL2mLSAAAAD1BMVEUqb6NHcEwEDBEsdq4teLHhu74uAAAABXRSTlPgAPucR2ZiTHoAAA3jSURBVHja7N3tbhs3EIXhmeXc/zUXaNMktqXVfpCHs5yX/VEggAHlwYvDlRFb5o84ERHt32PNfp1m9t8fRUTEM/4elp35X+Jj5z95uK8626XzrzrcZ6Tt9slpbgtKJza3TNQ25GQiT8I9ijobuWWgHmz9e1jgDgn1n8grc2utM4hbKevp4lbNeq64VcSeB24lraeJW1nsKeBS7ghLd7TiVjXsOeBWHVsLbmArwQ1sJbiBrQQ3sJXgo7kfhK0AN7C/gT+WO+yRJx7JHc0eegYuirEjykUxdkS5KMaOKBfFSFu5KEbaysCNtJWBG2krAzfSVj6idOVutuBpSbnDFj2RkXtZ7Z6BG0Oi9DbSVg6Koa30NoZEOSiG9uGTgjuszIn53IW0O3gb2soBN2Zb6W1oK70NbeUDyp0vtqJnDreVPaHnDjO8ddxmeMu4wwxvGXd57avehrbS29htpbfRttLbaFvpbWgr31+e/ooG8g1vQ1v5/UFDW+ltaCu9jUdApbehrXwcNLSV3sYDt/Jx0Lgmld6GtvK6NIZbOd+GttLbuCaV820Mt3K+jSlRehvayvk2hls538ZwK+fEmBLlnBhTovQ2pkQ5J8aUKL3tSdrbf//9+t8T58TyT8n24aSCb3e4I7n0F/UneFtW7e3SyT4nlnFKtlsnc96WLe6tx0mbt6V6g7N1PCm/d2J5pmTrfRLOiWWZkm3IyTYnliLubeBJlbcliHsbfBLlbbPvyU1x0tyWNjfuTXWSzInNjHtTnhRzYvPuyU19EuRt06Zkm3Cm522T4t4mncl525S4t3lnbt42I+5t6pmZt+nj3qafeXmbOu4tw5mWt4nj3pKcSXmbNu5tK+TdjnBHBWyNdxzgbjW0FeDtAHcZbYF3fORuZbAF3u0jdyXt8eDxgTtqaY/2bh+4q2mP9t7njnLag71jl7uVwx7tvccdFbXHescOdyupPdS77XAX1R7q/Z47qmqP9G5vuVtZ7YHeb7mjsPZA73jD3Sprj/NucEu9X3NHce1h3vGSu1XXHuXdXnKjPcr7FXegPco7XnA3tEdxtxfcaI/z/skdcI/zjh/cDe1x3u0HN9ojvb9zB9ojuQNupXf7xt3QHur9jRvtsdzxhTvgHuv9lbuhPda7DeHe4N4db+u7JRveu2vSl3vb8D7A3dAezd3glnr/4Q60RWsCt8r7D3dDe7x3g1ua929utBXe/3MH3Aru6Mm9bXgf425oK7gb3FLvX9xsiZI70NZ4B9yP5N7gPnZXWpebcsNbyL3BffCutB4PJhvecOfjDjcPtOFe0rsL9wb34UcTu/9gsuEN96rcG9zHnwTNiVvnDbeUO25zb3Cf4Q644V7UG24pd7vLvcF9irvBrfOGG264q2vD/dDvUsGtfTaBW/pdQbifwr3BrRyTDW/qZkzwhnvOGx24H1L3Breybrjhzszd4NbmDTfcq3IzJnDDDXcn7oD7Idwb3NJ/tAa3kpu6qTs5t6P9EG7qPntu/eQZdUu5qfvsYzd1P4ebui9w8+AN95rcAbeam/c5cK/JffMX28ENd17uBreeO+BW3ZRwy7kd7mdw8++7Tz6Y3PzsBbjP3ZRw67m5K+Fe8qa8+ZlncEu5+Zn4cw8mdz9AEe5T0w33BG7uSsGWwC2/Kd3c3Z27UnNT3v6ceLjhTntT/uJmvDU35W1ufsPxmZvyFzd3pZab8ZbclHBLp/t/bsZbsiVwT+Hmrhyr/ZvZ7443n3l2fLrhnsPNeA/dkvjGzU+zarlZE8FNCbdEu/3g5jc/CLYEboX2C+5bn1sJ97Hp/oubX7k2frr/4mZNhsXdm9vgPjTdf3Ez3qO0/zb2LuNtcB/Zkr+5WZNBcQ/gNrgPTPff3A73EO0vxN5pvA3uz1vyhZs1GRL3GG6D++N0f+FmTUZofxHuyG1wf9qSr9w318TQ/rAlX7kd7u7ae9wN7+7cDrdQu+1w3x1vg3t3S75xu+HdV/u7r3ddE0N7b0u+cwd5P4vb0H4/3d+576+Jof1+ugdwG9xvt+QHd4c1MbTfbckPbrfy3jZuS35yt+rcPbXbR+6onvcDuQ3tl9P9k7vLmjzXu6v2T1y4B2q3A9x91sTQfrElL7jdynp31n5l64PW5IneNnpLXnGHFfW24VvyitutprdN4m4lvbtrNz/GHVbQ26Zxu9Xz7q/9aktec7dy3qaJ+zV3WDFvW4fbamq/3JLX3F3XJL23jTk+i9sqarcT3GFlvAdpv96SN9y9884LPkr7jauK24ppt1PcYSW8h2m/2ZJ33G4FvG3g8XPczZYHH6ndTnKHre49Uvvdlrzl9kGvowS2vVd15Zqk8R6s3U5zh63rbaNPnOb2cS9mee0dVFevyWzw8djvt2SHO2xFb1OcuMDtY1/Swtp7pj5lTeaAa7B3tmSPO4a/riWx97Zkj9sFr2xBbNsl9Zl5y8CF2HtbMp9bAW7SExe5h1+WGnATH8/OPVDc5Kdd5nbly1wDe39LPnA37St9vvWHLfnAHfIX+3DrD1uSjruLuE08cYNbvSYdyG3u2Y/7E3dMfOWPo77P7bNf/nOgD1yUn7lbkr/G9hLe8jgfivsjdxin20X5mdsh7Lgln7kbhv225DM3a9JxSz5zk3fHLYFbuiUHuLks+23JEW7y7rYlR7i5LLttyRFu1qRb3Ie4WZNecR/iZk06XZTHuFmTXltyjJs16bQlx7hZk05bcoybvDttyUFu8u6zJQe5uSz7bMlRbtakS9xHuVmTLnEf5WZNelyUx7lZkx5bcpibNemxJYe5ybvHlhznJu8OcR/n5rLUcrMmty/KM9ysyf24T3CzJrcvylPc5H17S+CWbskZbi7L23Gf4ibvu3Gf4uayvHlRnuQm75tbArd0S85xc1nejPskN3nfi/skN5flrYvyNDdrcmtLznKT960tOc1N3nfiPs3NZXkn7tPcrMmNi/ICN2tyY0vOc5P3jS25wE3e1+O+wM1leT3uC9ysyeWL8hI3a3J5S65wk/flLbnETd5X477EzWV5Ne5L3KzJxYvyIjd5X9ySa9zkfTHui9xcltfivsjNmly6KK9yk/dFt4tfFsSt5HbilnIXX5Mm5na2RMrdiFvJHcSt5C69Jq7nDrZEye1siZS7EbeSO4hbyV02b5/DHcSt5HbilnKXXJM2jdvZEil3I24ldxC3krtg3j6TO4hbye3ELeUutiZtMrezJVLuRtxK7iBuJXepvH0+dxC3ktuJW8pdZk1aCm5nS6TcjbiV3EHcSu4aefeIuw93ELeSu0Tenoc72BIltxO3lLsRt5J7+bwjF3cjbiV3ELeSe/G8PRt3ELeS24lbyr1w3i0htxO3lLsRt5J72bwjJ3cjbiV3ELeSe828e8bdlzuIW8m9ZN6elzuIW8ntxC3lXi7vlprbiVvK3Yhbyb1Y3pGduxG3kjuIW8m9Ut7d4x7AHcSt5F4ob38CdxC3ktuJW8odXJRKbiduKXcjbiW3c1FKuRtxK7mduKXcjbiV3EHcSu6n5z0o7mHcQdxK7ofn7U/jDuJWcjtxS7mDi1LJ7cQt5Q7iVnI7cUu5G3EruR+adzyVuxG3ktuJW8rdiFvJHcSt5H5e3mPjHs0dxK3kflreg+Mezh3EreR+WN7+dO4gbiX3o/L253MHcSu5nbil3EHcSm4nbin3Q/Jui3A7cUu5g7iV3E7cUu5G3EpuJ24pdyNuJXf6vGMt7kbcSm4nbil3I24ltxO3lLsRt5I7iFvJnTdvXdxK7iBuJXfWvIVxS7mjfNxS7px5K+PWckf1uLXcGfOWxi3mjuJxi7kT5u0rc0ftuNXc6fL2tbmjdNxy7mR5++rcUTluPXeqvH197igc9wTuRHl7Be6oG/cM7jR5ew3uKBv3FO4keXsV7qga9xzuFHl7He4oGvck7gR5eyXuqBn3LO7peXst7igZ9zTuyXl7Ne6oGPc87ql5ez3uKBj3RO6JeXtF7qgX90zuaXl7Te4oF/dU7kl5e1XuqBb3XO4peXtd7igW92Rufd7NK3NHrbhnc6vznhz3dO4oFfd0bm3es+Oezx2V4p7Prcx7etwJuKNQ3Am4dXnPjzsDd9SJOwO3Ku8EcafgjjJxp+DW5J0h7hzcXiXuJNytSNxJuL1I3Fm4W424s3B7jbjTcLcScafhHpy3wy3Mu8GtzNvhFr6Vb3Ar83a4hXk3uJV5O9zCvANuZd4OtzDvgFv5XsfhFuYdcCvzdriFeQfcwrybwy3MO+AW5p0t7nzcsXLc+bh75p0u7oTcvnDcGbnbunFn5PY13+Gk5W7Lxp2S25eNOyd3rBp3Tm5fNe6k3LFo3Em5fdG4s3LHeu9wMnPffhh0uIV5B9zKvB1uYd4BtzDv5nAL8w64hXnnjTszt68Xd2rutlzcqbl9ubhzc7fV4s7N7Su9w3kAdywWd3JuXyzu7Nyx0j2Zn/v0belwC/MOuIV5N4dbmHfALcw7fdwP4PaF4n4Cd1sn7idw+z/t1rEJwAAMA0GEtf/MqQMpUgleaIXjsVUyAincrokbwa2auBncbombwa2WuCHcbhiBHO4fY1DjDubtcQfzPo07mLfHHcybEjeHWw1xg7hdEDeIW/QRCOM2/pSguMWPG8VtfNwo7u8xeBp3MG+PO5g3Km4Yt+Bx07iPHTeNW+ARSOQ2Om4ct9Bx87jN/ZNE7te31LiDeXvcwbxP4w5+S487mPdp3MG8Ne7gt/S4k+dE4w7m7XEH8z6NO5g3M249Mb2uvvHsSzsAAAAASUVORK5CYII=" alt="pin for map">' +
        `<div style="display: flex; flex-direction: column; font-size: 1.2em">
      <span><b>Latitude: </b>${latlng.lat.toFixed(5)}°</span>
      <span><b>Longitude: </b>${latlng.lng.toFixed(5)}°</span>
      <span><b>Valor: </b>${value.toFixed(3)}</span>
      <a href="javascript:void(0)" id="infowindow-${latlng.lat + '' + latlng.lng}">${openPanelabel}</a>
  </div>
</div>`
// add this line to open side panel:
// 
    );
}

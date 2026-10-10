# Repository Markdown link audit

Generated: `2026-10-10T11:40:48.667967+00:00`. First-pass reachability observations; rerun against final documentation before publishing.

- Markdown sources: **81**
- Exact external URL identities: **201** (287 occurrences)
- Local link occurrences: **266**

## Computed classifications

| Kind | Classification | Count |
| --- | --- | ---: |
| external | api_request_required | 17 |
| external | auth_required | 3 |
| external | blocked | 31 |
| external | broken_http | 14 |
| external | dns_error | 25 |
| external | http_error | 2 |
| external | network_error | 2 |
| external | not_requested | 3 |
| external | reachable | 77 |
| external | server_error | 2 |
| external | timeout | 23 |
| external | tls_error | 2 |
| local | local_ok | 266 |

## Broken prose links and local failures

- **broken_http** `https://data.komdigi.go.id/opendata` — apis/tier4-ministry/komdigi/README.md:23:29, apis/tier4-ministry/komdigi/README.md:36:14
- **broken_http** `https://data.komdigi.go.id/opendata/desa-broadband` — apis/tier4-ministry/komdigi/README.md:24:29
- **broken_http** `https://djpb.kemenkeu.go.id/portal/id/data/apbn-realisasi` — apis/tier6-financial/djpb-budget/README.md:23:29, apis/tier6-financial/djpb-budget/README.md:35:14
- **broken_http** `https://djpb.kemenkeu.go.id/portal/id/data/apbn-realisasi.html` — apis/tier1-open-apis/apbn-kemenkeu/README.md:23:29
- **broken_http** `https://kkp.go.id/djprl/p4k/page/3-data-kawasan-konservasi` — apis/tier4-ministry/kkp-fisheries/README.md:23:29
- **broken_http** `https://ksei.co.id/publikasi/statistik` — apis/tier6-financial/ksei-stats/README.md:23:29, apis/tier6-financial/ksei-stats/README.md:35:14
- **broken_http** `https://oss.go.id/informasi/cari-nib` — apis/tier2-scrapeable/oss-nib/README.md:23:29
- **broken_http** `https://pasal-mcp-server-production.up.railway.app` — apis/tier7-civil-society/pasal-id/README.md:23:29
- **broken_http** `https://simas.kemenag.go.id/search` — apis/tier4-ministry/kemenag/README.md:23:29
- **broken_http** `https://www.esdm.go.id/id/statistik-dan-riset` — apis/tier4-ministry/esdm-energy/README.md:23:29, apis/tier4-ministry/esdm-energy/README.md:36:14
- **broken_http** `https://www.esdm.go.id/id/statistik-dan-riset/publikasi/handbook-of-energy` — apis/tier4-ministry/esdm-energy/README.md:24:29
- **broken_http** `https://www.ksei.co.id/files/statistik/investor-statistics-2025-01.xlsx` — apis/tier2-scrapeable/ksei/README.md:51:14
- **broken_http** `https://www.ksei.co.id/publikasi/laporan-tahunan` — apis/tier2-scrapeable/ksei/README.md:73:21
- **broken_http** `https://www.ksei.co.id/publikasi/statistik` — apis/tier2-scrapeable/ksei/README.md:23:29, apis/tier2-scrapeable/ksei/README.md:36:18

## Other external observations requiring review

- **timeout** (HTTP none) `https://ahu.go.id` — apis/tier2-scrapeable/ahu-company/README.md:4, apis/tier2-scrapeable/ahu-company/README.md:28
- **timeout** (HTTP none) `https://ahu.go.id/pencarian/cari-pt` — apis/tier2-scrapeable/ahu-company/README.md:46, apis/tier2-scrapeable/ahu-company/README.md:54
- **auth_required** (HTTP 401) `https://aleph.occrp.org/api/2/entities` — apis/tier5-transparency/occrp-aleph/README.md:36
- **server_error** (HTTP 503) `https://api-jdih.perpusnas.go.id` — apis/tier1-open-apis/jdih-bpk/README.md:29, apis/tier1-open-apis/jdih-bpk/README.md:44
- **api_request_required** (HTTP 404) `https://api.bmkg.go.id/publik/prakiraan-cuaca` — apis/tier1-open-apis/bmkg/README.md:10, apis/tier1-open-apis/bmkg/README.md:24, references/bmkg-weather.md:7
- **auth_required** (HTTP 401) `https://api.opencorporates.com/v0.4/companies/search` — apis/tier5-transparency/opencorporates/README.md:35
- **timeout** (HTTP none) `https://atrbpn.go.id` — apis/tier4-ministry/atr-bpn/README.md:4, apis/tier4-ministry/atr-bpn/README.md:28
- **api_request_required** (HTTP 404) `https://aturan.org/api/v1` — apis/tier7-civil-society/aturan-org/README.md:26
- **tls_error** (HTTP none) `https://bappebti.go.id` — apis/other/bappebti/README.md:4
- **tls_error** (HTTP none) `https://bappebti.go.id/pialang_berjangka` — apis/tier2-scrapeable/ojk/README.md:92
- **timeout** (HTTP none) `https://bo.ahu.go.id` — apis/tier2-scrapeable/ahu-company/README.md:85, apis/tier5-transparency/ahu-bo/README.md:4, apis/tier5-transparency/ahu-bo/README.md:28
- **timeout** (HTTP none) `https://bo.ahu.go.id/search` — apis/tier5-transparency/ahu-bo/README.md:39
- **timeout** (HTTP none) `https://cekbansos.kemensos.go.id/` — docs/monitor-only-endpoints.md:33
- **timeout** (HTTP none) `https://data-apbn.kemenkeu.go.id` — apis/tier1-open-apis/apbn-kemenkeu/README.md:4, apis/tier1-open-apis/apbn-kemenkeu/README.md:35
- **dns_error** (HTTP none) `https://data.baliprov.go.id` — apis/tier3-regional/opendata-bali/README.md:4, apis/tier3-regional/opendata-bali/README.md:28
- **dns_error** (HTTP none) `https://data.baliprov.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:313
- **dns_error** (HTTP none) `https://data.baliprov.go.id/dataset` — apis/tier3-regional/opendata-bali/README.md:47
- **blocked** (HTTP 403) `https://data.bnpb.go.id` — apis/tier1-open-apis/bnpb-disaster/README.md:4, apis/tier1-open-apis/bnpb-disaster/README.md:28
- **api_request_required** (HTTP 404) `https://data.go.id/api/3/action/organization_list` — apis/tier1-open-apis/data-go-id/README.md:76
- **api_request_required** (HTTP 404) `https://data.go.id/api/3/action/package_search` — apis/tier1-open-apis/data-go-id/README.md:43, apis/tier1-open-apis/djpb-treasury/README.md:51
- **api_request_required** (HTTP 404) `https://data.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:307
- **api_request_required** (HTTP 404) `https://data.go.id/api/3/action/package_show` — apis/tier1-open-apis/data-go-id/README.md:62
- **api_request_required** (HTTP 404) `https://data.go.id/api/3/action/tag_list` — apis/tier1-open-apis/data-go-id/README.md:86
- **blocked** (HTTP 403) `https://data.inaproc.id/docs/dokumentasi/guides/migration-from-isb` — docs/monitor-only-endpoints.md:29
- **blocked** (HTTP 403) `https://data.jabarprov.go.id` — apis/tier3-regional/opendata-jabar/README.md:29
- **blocked** (HTTP 403) `https://data.jabarprov.go.id/api/bigdata/bps/v2` — apis/tier3-regional/opendata-jabar/README.md:63
- **dns_error** (HTTP none) `https://eiti.esdm.go.id` — apis/tier5-transparency/eiti-indonesia/README.md:28
- **timeout** (HTTP none) `https://elhkpn.kpk.go.id` — apis/tier2-scrapeable/kpk-lhkpn/README.md:4
- **timeout** (HTTP none) `https://elhkpn.kpk.go.id/portal/user/login` — apis/tier2-scrapeable/kpk-lhkpn/README.md:24, docs/source-review-2026-10-10.md:295
- **timeout** (HTTP none) `https://emis.kemenag.go.id` — apis/tier4-ministry/kemenag/README.md:35
- **dns_error** (HTTP none) `https://geoportal.indonesia.go.id` — apis/tier7-civil-society/geoportal-onemap/README.md:4, apis/tier7-civil-society/geoportal-onemap/README.md:28
- **dns_error** (HTTP none) `https://geoportal.indonesia.go.id/home` — apis/tier7-civil-society/geoportal-onemap/README.md:39
- **dns_error** (HTTP none) `https://geoservices.ina-sdi.or.id` — apis/tier1-open-apis/big-geospatial/README.md:30
- **blocked** (HTTP 403) `https://inaproc.id` — apis/tier1-open-apis/lpse-inaproc/README.md:4
- **blocked** (HTTP 403) `https://inaproc.id/satudata` — docs/monitor-only-endpoints.md:30
- **server_error** (HTTP 502) `https://inarisk.bnpb.go.id/api/irbi` — apis/tier1-open-apis/bnpb-disaster/README.md:60
- **api_request_required** (HTTP 404) `https://inarisk.bnpb.go.id/api/risk/score` — apis/tier1-open-apis/bnpb-disaster/README.md:43, apis/tier7-civil-society/sigap-inarisk/README.md:39
- **dns_error** (HTTP none) `https://indolii.or.id` — apis/tier7-civil-society/indolii/README.md:4, apis/tier7-civil-society/indolii/README.md:28
- **timeout** (HTTP none) `https://infopemilu.kpu.go.id` — docs/source-review-2026-10-10.md:301
- **timeout** (HTTP none) `https://ispu.ahu.go.id` — apis/tier2-scrapeable/ahu-company/README.md:29
- **blocked** (HTTP 403) `https://jakartasatu.jakarta.go.id/server/rest/services/apps/Jakartasatu/MapServer` — apis/tier3-regional/satu-data-jakarta/README.md:89
- **blocked** (HTTP 403) `https://jdih.bpk.go.id` — apis/tier1-open-apis/jdih-bpk/README.md:4
- **timeout** (HTTP none) `https://jdihn.go.id/` — docs/monitor-only-endpoints.md:46
- **dns_error** (HTTP none) `https://katalog.data.go.id/api/3/action/package_search?rows=0` — docs/monitor-only-endpoints.md:37
- **network_error** (HTTP none) `https://map.big.go.id/wfs` — apis/tier1-open-apis/big-geospatial/README.md:29, apis/tier1-open-apis/big-geospatial/README.md:42, apis/tier7-civil-society/geoportal-onemap/README.md:46
- **network_error** (HTTP none) `https://map.big.go.id/wms` — apis/tier1-open-apis/big-geospatial/README.md:92
- **auth_required** (HTTP 401) `https://mcp.aturan.org/mcp` — apis/tier7-civil-society/aturan-org/README.md:44, docs/source-review-2026-10-10.md:183, mcp-servers/README.md:22
- **blocked** (HTTP 403) `https://mkri.id` — apis/tier2-scrapeable/putusan-mk/README.md:4, apis/tier2-scrapeable/putusan-mk/README.md:28, apis/tier2-scrapeable/putusan-mk/README.md:77
- **blocked** (HTTP 403) `https://mkri.id/index.php` — apis/tier2-scrapeable/putusan-mk/README.md:45, apis/tier2-scrapeable/putusan-mk/README.md:69, apis/tier2-scrapeable/putusan-mk/README.md:99
- **blocked** (HTTP 403) `https://mkri.id/index.php?page=web.Putusan` — apis/tier2-scrapeable/putusan-mk/README.md:29
- **dns_error** (HTTP none) `https://monev.anggaran.kemenkeu.go.id` — apis/tier1-open-apis/apbn-kemenkeu/README.md:37
- **timeout** (HTTP none) `https://ojk.go.id` — apis/tier2-scrapeable/ojk/README.md:4, apis/tier2-scrapeable/ojk/README.md:28
- **timeout** (HTTP none) `https://ojk.go.id/en/berita-dan-kegiatan/siaran-pers/Pages/Bappebti-Transfers-Regulation-and-Supervision-Duties-on-Digital-Financial-Assets-Crypto-Assets-and-Derivatives-to-OJK-BI.aspx` — docs/source-review-2026-10-10.md:297
- **timeout** (HTTP none) `https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/Nota-Kesepahaman-OJK-Bappebti-2026.aspx` — docs/source-review-2026-10-10.md:317
- **api_request_required** (HTTP 404) `https://opendata.bandung.go.id/api/3/action` — apis/tier3-regional/opendata-bandung/README.md:40
- **api_request_required** (HTTP 404) `https://opendata.bandung.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:312
- **blocked** (HTTP 403) `https://opendata.jabarprov.go.id` — apis/tier3-regional/opendata-jabar/README.md:4, apis/tier3-regional/opendata-jabar/README.md:28
- **blocked** (HTTP 403) `https://opendata.jabarprov.go.id/api/3/action` — apis/tier3-regional/opendata-jabar/README.md:41
- **blocked** (HTTP 403) `https://opendata.jabarprov.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:309
- **blocked** (HTTP 403) `https://opendata.jatimprov.go.id` — apis/tier3-regional/opendata-jatim/README.md:4, apis/tier3-regional/opendata-jatim/README.md:28
- **blocked** (HTTP 403) `https://opendata.jatimprov.go.id/api/3/action` — apis/tier3-regional/opendata-jatim/README.md:40
- **blocked** (HTTP 403) `https://opendata.jatimprov.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:310
- **blocked** (HTTP 403) `https://opengovindonesia.org` — apis/tier7-civil-society/ogp-indonesia/README.md:4, apis/tier7-civil-society/ogp-indonesia/README.md:28
- **http_error** (HTTP 406) `https://pasal-mcp-server-production.up.railway.app/mcp` — apis/tier7-civil-society/pasal-id/README.md:37
- **blocked** (HTTP 403) `https://peraturan.bpk.go.id` — apis/tier1-open-apis/jdih-bpk/README.md:28, apis/tier7-civil-society/aturan-org/README.md:18, docs/source-review-2026-10-10.md:187, docs/source-review-2026-10-10.md:318
- **blocked** (HTTP 403) `https://peraturan.bpk.go.id/Search` — apis/tier1-open-apis/jdih-bpk/README.md:66
- **timeout** (HTTP none) `https://ppid.bps.go.id` — apis/tier2-scrapeable/ppid/README.md:43
- **timeout** (HTTP none) `https://ppid.bps.go.id/daftar-informasi-publik` — apis/tier2-scrapeable/ppid/README.md:56
- **dns_error** (HTTP none) `https://ppid.kemenkeu.go.id` — apis/tier2-scrapeable/ppid/README.md:41
- **dns_error** (HTTP none) `https://ppid.kemenkumham.go.id` — apis/tier2-scrapeable/ppid/README.md:42
- **dns_error** (HTTP none) `https://ppid.kominfo.go.id` — apis/tier2-scrapeable/ppid/README.md:4, apis/tier2-scrapeable/ppid/README.md:28, apis/tier2-scrapeable/ppid/README.md:40
- **dns_error** (HTTP none) `https://ppid.kominfo.go.id/tracking` — apis/tier2-scrapeable/ppid/README.md:82
- **dns_error** (HTTP none) `https://ppid.ojk.go.id` — apis/tier2-scrapeable/ppid/README.md:45
- **blocked** (HTTP 403) `https://putusan3.mahkamahagung.go.id` — apis/tier1-open-apis/putusan-ma/README.md:4, apis/tier1-open-apis/putusan-ma/README.md:28, apis/tier1-open-apis/putusan-ma/README.md:40
- **dns_error** (HTTP none) `https://referensi.data.kemdikbud.go.id` — apis/tier4-ministry/kemendikdasmen/README.md:28
- **dns_error** (HTTP none) `https://referensi.data.kemdikbud.go.id/api/sekolah` — apis/tier4-ministry/kemendikdasmen/README.md:34
- **api_request_required** (HTTP 404) `https://satudata.kemnaker.go.id/api/v1/bpjs-coverage` — apis/tier4-ministry/kemnaker/README.md:85
- **api_request_required** (HTTP 404) `https://satudata.kemnaker.go.id/api/v1/tenaga-kerja` — apis/tier4-ministry/kemnaker/README.md:64
- **api_request_required** (HTTP 404) `https://satudata.kemnaker.go.id/api/v1/ump` — apis/tier4-ministry/kemnaker/README.md:41
- **dns_error** (HTTP none) `https://satudata.kkp.go.id` — apis/tier4-ministry/kkp-fisheries/README.md:4, apis/tier4-ministry/kkp-fisheries/README.md:35
- **dns_error** (HTTP none) `https://satudata.kkp.go.id/api/v1/harga-ikan` — apis/tier4-ministry/kkp-fisheries/README.md:81
- **api_request_required** (HTTP 404) `https://satudata.surabaya.go.id/api/3/action` — apis/tier3-regional/satu-data-surabaya/README.md:41
- **api_request_required** (HTTP 404) `https://satudata.surabaya.go.id/api/3/action/package_search?rows=0` — docs/source-review-2026-10-10.md:311
- **dns_error** (HTTP none) `https://sigap.bnpb.go.id` — apis/tier7-civil-society/sigap-inarisk/README.md:4, apis/tier7-civil-society/sigap-inarisk/README.md:28
- **blocked** (HTTP 403) `https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/AlertList` — apis/tier2-scrapeable/ojk/README.md:56
- **blocked** (HTTP 403) `https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search` — apis/tier2-scrapeable/ojk/README.md:79
- **blocked** (HTTP 403) `https://sikepo.ojk.go.id` — apis/tier6-financial/ojk-sikepo/README.md:4
- **blocked** (HTTP 403) `https://sipp.pn-medankota.go.id/` — docs/monitor-only-endpoints.md:43
- **blocked** (HTTP 403) `https://sipp.pn-semarangkota.go.id/` — docs/monitor-only-endpoints.md:45
- **blocked** (HTTP 403) `https://sirup.inaproc.id` — docs/monitor-only-endpoints.md:31
- **dns_error** (HTTP none) `https://statistik.kkp.go.id` — apis/tier4-ministry/kkp-fisheries/README.md:36
- **dns_error** (HTTP none) `https://statistik.kkp.go.id/home.php` — apis/tier4-ministry/kkp-fisheries/README.md:55
- **dns_error** (HTTP none) `https://tracker.antikorupsi.org` — apis/tier5-transparency/icw-corruption/README.md:28
- **timeout** (HTTP none) `https://waspadainvestasi.ojk.go.id` — apis/tier6-financial/satgas-waspada/README.md:4, apis/tier6-financial/satgas-waspada/README.md:28
- **timeout** (HTTP none) `https://waspadainvestasi.ojk.go.id/` — apis/tier6-financial/satgas-waspada/README.md:40
- **api_request_required** (HTTP 404) `https://web-api.invoice-kohyo.nta.go.jp/1/num` — apis/reference/nta/README.md:52
- **timeout** (HTTP none) `https://webapi.bps.go.id/documentation` — docs/source-review-2026-10-10.md:292
- **timeout** (HTTP none) `https://webapi.bps.go.id/v1/api/list` — apis/tier1-open-apis/bps/README.md:25
- **http_error** (HTTP 418) `https://www.bgn.go.id/operasional-sppg` — docs/monitor-only-endpoints.md:32
- **blocked** (HTTP 403) `https://www.bps.go.id` — apis/tier1-open-apis/bps/README.md:4
- **blocked** (HTTP 403) `https://www.idx.co.id` — apis/tier1-open-apis/idx/README.md:4, apis/tier1-open-apis/idx/README.md:28
- **blocked** (HTTP 403) `https://www.idx.co.id/primary/StockData/GetStockData` — apis/tier1-open-apis/idx/README.md:84
- **blocked** (HTTP 403) `https://www.idx.co.id/primary/TradingSummary/GetTradingSummary` — apis/tier1-open-apis/idx/README.md:92
- **api_request_required** (HTTP 404) `https://www.invoice-kohyo.nta.go.jp/web/api/` — apis/reference/nta/README.md:39
- **timeout** (HTTP none) `https://www.ksei.co.id` — apis/tier2-scrapeable/ksei/README.md:4, apis/tier2-scrapeable/ksei/README.md:35
- **dns_error** (HTTP none) `https://yankes.kemkes.go.id` — apis/tier4-ministry/kemenkes/README.md:4, apis/tier4-ministry/kemenkes/README.md:28
- **dns_error** (HTTP none) `https://yankes.kemkes.go.id/api/fasyankes` — apis/tier4-ministry/kemenkes/README.md:34

## Safety and freshness

Allowlisted root Markdown and docs/apis/references/mcp-servers/status/examples only. Caches, dependencies, private scratch, symlinks and audit reports are excluded. Credential-bearing, templated, dummy and non-public literal-address targets are not requested. Redirect targets receive the same screening. No response body or raw error text is retained. Verified-TLS GETs have explicit total per-URL timeout, byte and redirect caps, with one in-flight request per host.

403 means observed blocked; 401 authentication required; 429 rate limited. Transport errors are not HTTP outages. Parameterized/API/POST examples are distinguished from confirmed broken prose links. External fragment validity, authentication, POST functionality and CAPTCHA behavior are not tested.

Complete occurrences, skipped reasons, redirect observations and exact SHA-256 source snapshots are in the sibling JSON report. Compare hashes to current files before treating this report as fresh.

## Source SHA-256 snapshots

| Source | SHA-256 |
| --- | --- |
| AGENTS.md | `26c25949a4e9c2ede83755a122d845f3fe8d93a753f56e1601bfcce6ec89f9f5` |
| CONTRIBUTING.md | `efa4bfbdb36baba8297fcc50b9c184f88faff364042a1b08755fdac9ca4286dd` |
| README.md | `1ace5c7fc87a8621b7e807f52d3e76591afa38cf9493a0518e6348f5b955bb5c` |
| SECURITY.md | `d3abedce2e91618e06db8e53a07bc4dee3d652bc82b3e611633a7133794212f8` |
| SKILL.md | `52a72b40494dd94fa17d81e63c12575f038024b8ece3452fefbe6850617c5b83` |
| apis/other/bappebti/README.md | `8bbf38c1b6ba164ad45e30d70404603471d95f497f589cd7114d56e19e3ccfab` |
| apis/reference/nta/README.md | `36c07b572f44476622043206b2082656f8ae3e7fbbe058b955cf63524e3f5bae` |
| apis/tier1-open-apis/apbn-kemenkeu/README.md | `3f7c348cfc17ac44afdec1f41fad4acd3c9a9f890b11b00cde8a019044126bf0` |
| apis/tier1-open-apis/bank-indonesia/README.md | `8604d55b0ea0bb567aa71e986edfd555a643615524d6ee17e06e1c16a09d9ef5` |
| apis/tier1-open-apis/big-geospatial/README.md | `3c2e7be859b7daea1094797c0e25634b3b39938e587330787d5cd7e461f0b44e` |
| apis/tier1-open-apis/bmkg/README.md | `3cddd536b9bee85a7661ec174c4c42ab834b8339c39f7428316365f3947a9627` |
| apis/tier1-open-apis/bnpb-disaster/README.md | `5bdbc6597420e83378ad6184c54e795a000c51a747fac053f0c666ab0b826bce` |
| apis/tier1-open-apis/bps/README.md | `29513401d3244eb914ce661c0fc71b490bb9c5eeecd1c515e98c5fdbd0da832f` |
| apis/tier1-open-apis/data-go-id/README.md | `80d0573282e5fb69234cd36e214ac207fd4c48234365f7cfcd6ab40c3cac6cbe` |
| apis/tier1-open-apis/djpb-treasury/README.md | `2561fefe69b4e67dab1beeb4f4bee9aeb8f92112a60a92dae9332ff24926558d` |
| apis/tier1-open-apis/idx/README.md | `28a75e74a836cd258f496c65331da662d81a9e30c867b985ae2cd35d12c99c9e` |
| apis/tier1-open-apis/jdih-bpk/README.md | `e6222e7823a762c4950b7dd5aa55d604560b17d26ee6b1134aa077e29ddf983b` |
| apis/tier1-open-apis/lpse-inaproc/README.md | `8ae0453cf17367be15095542a7c2c930e96f172b162c46f0cbc5b315a610e2b2` |
| apis/tier1-open-apis/putusan-ma/README.md | `f2548fe2ab2e05f334818c4898191c1d60aaf9fd4a9a881570717098dbae6c81` |
| apis/tier2-scrapeable/ahu-company/README.md | `9892ad1c9e6116720ae0040ad82ecf7d3ff3e9e2fe7b03bb029b949adff72ef9` |
| apis/tier2-scrapeable/bpjph/README.md | `a1b733a141828e84cb46dc810f6df1ad7e3e8ea4adfeee1e716bfc062d90c4a2` |
| apis/tier2-scrapeable/bpom/README.md | `4ee7f02fc90dad50d5be32424c4871a1c245aa4390b1eae7369d23878c8eb4c5` |
| apis/tier2-scrapeable/kpk-lhkpn/README.md | `859bf072804ba3e782c4af06fc3bcc846297baf4878fb554ea625b290116184c` |
| apis/tier2-scrapeable/ksei/README.md | `17be368f2331c0eeb9f7979c240c0a20bf2c43abe1fae92ccf3ae77c39a2f291` |
| apis/tier2-scrapeable/ojk/README.md | `76e9344954af48c6c84768e0af1b9981b7bb9f99794a3412571c8b67a248d784` |
| apis/tier2-scrapeable/oss-nib/README.md | `e8b1a742c736236e908c485b1d35a4ce63be783bbbbb300263b4a42b28fde3be` |
| apis/tier2-scrapeable/pajak-djp/README.md | `62681876880788f07f09633789baa97a094d9ee4f1354135de5469f0faba9b8c` |
| apis/tier2-scrapeable/ppid/README.md | `30ac85d3c7292725096f8e99b294d911603e96ba7493f62da152274069f26f3f` |
| apis/tier2-scrapeable/putusan-mk/README.md | `961e696297802409115da726eaa0c9b87dbdd77275cfd9b159244a730ed86710` |
| apis/tier3-regional/opendata-bali/README.md | `8656fd4167d90ca4bb827e93602c4960fe90b2f744657eabbf16bf0a734fa2fc` |
| apis/tier3-regional/opendata-bandung/README.md | `679dc05e0ccebc99eb1880f1eaef779dfac7aa90e60433b3b1853f9adcc79b65` |
| apis/tier3-regional/opendata-jabar/README.md | `8109c9c5e6be9aeb0e78db175d900dd20dc47d2e5cd38188fa1d53ce6ac37a9e` |
| apis/tier3-regional/opendata-jatim/README.md | `4980aed349f40723f07967bf789f9d2fc723aa974ae5a608d97663cc2c74262e` |
| apis/tier3-regional/satu-data-jakarta/README.md | `a66512f8335fc0a0a723ad6294c73211866fbad36daea8f99d9f79072aa1cf88` |
| apis/tier3-regional/satu-data-surabaya/README.md | `e1d9fd8b554413bdca87cb488fcb08a22c34bd5f5ddc80cac4b85d8c6fbc6ff9` |
| apis/tier4-ministry/atr-bpn/README.md | `68bb049526649b59897fe0c785ff0294dfb165eef62167fc7a9399a0dc5cc734` |
| apis/tier4-ministry/esdm-energy/README.md | `8181f95090575bd83ac4ab4ffb589a4876856482ffbcfcae733e77034428216a` |
| apis/tier4-ministry/kemenag/README.md | `fbcb8bdc8a3d7d82f7173a6f15a7f55a10ba9b48026527d3a1ce5640f40c8919` |
| apis/tier4-ministry/kemendikdasmen/README.md | `8008dfc44ea48517d42fbf3d328f9c7186b2e11c07f0dae279750cf930d6156e` |
| apis/tier4-ministry/kemenkes/README.md | `9757c372a5ae3282fdbe942956ea03131214f7d3c8ce03787b0b9fe2ac151a51` |
| apis/tier4-ministry/kemnaker/README.md | `e6d0f0ed2371914990bc7998633af55e662b0208f259f146fd395dca4b8364e2` |
| apis/tier4-ministry/kkp-fisheries/README.md | `b169d54b20160dea293d95c311aa3b543e150d90a9e31ded98587768c1802cd2` |
| apis/tier4-ministry/komdigi/README.md | `0efcdc9348ffd39830097becf66f953d088352a5ed3f0ed11ea633b893f36185` |
| apis/tier5-transparency/ahu-bo/README.md | `06defcf52b2b0f845a560bb6c2d35aaa07f98a8b5df4eb1be1c4921b6bbf62e5` |
| apis/tier5-transparency/eiti-indonesia/README.md | `bf16c48793ab40424246401801ec3722691a4b9d96fc431078c1f0d00d4ec59c` |
| apis/tier5-transparency/icw-corruption/README.md | `10eef932a56c5de8d3926c08c717dc1f722266cd717878bee7fd048ebef3bf38` |
| apis/tier5-transparency/occrp-aleph/README.md | `f283d0c21f35d7d8fad1bce95d054a640bd44912c92f17e1809f3fa1c6d9c4d5` |
| apis/tier5-transparency/opencorporates/README.md | `99d7bce87d2a55e9d2d3774dbaf70602c2ac12220711b89634fe1b3621d8fe82` |
| apis/tier6-financial/djpb-budget/README.md | `62d7977932586a90e740c3f5f738af3bb587f726e243ce50ccbf7b60ffd19507` |
| apis/tier6-financial/ksei-stats/README.md | `8ca90a6c19f0c13f683171628880b479cc736e7a16548d51cf89f9fd81d8346f` |
| apis/tier6-financial/ojk-sikepo/README.md | `8766d38af7b8c095d92899fff67b075fa808214e490a5947eeb964c7a6f168df` |
| apis/tier6-financial/satgas-waspada/README.md | `44e3b729cb742d394854366776252452f61527a7ec8a4735ba395ffe2e2e8847` |
| apis/tier7-civil-society/aturan-org/README.md | `b01ebabbed2d6cc26fe66ca69c84133dce794be059d649297dc3ba4614a2ca30` |
| apis/tier7-civil-society/geoportal-onemap/README.md | `9038c5438fed4321ab962c6f8797896be1ae05d17a7a87a7bb9fb9d3c0d85ecc` |
| apis/tier7-civil-society/indolii/README.md | `bcea4fadceeb419d2d66c6b04cc44053d3a5ab30a0330c8937b1ce58494a6296` |
| apis/tier7-civil-society/lapor/README.md | `db3c5d179d16e1cc14250f01932a58aa9dfc5fa426287ddbd61b07ef6a531d91` |
| apis/tier7-civil-society/ogp-indonesia/README.md | `0b3a10cb1f34c90844e9a94366dba698aee70022bbc04eca21d9d882d4e3d795` |
| apis/tier7-civil-society/pasal-id/README.md | `9bc4194db5ce42b12a35816dc9295496395be44d162637a6c0eaf6e0968b1742` |
| apis/tier7-civil-society/sigap-inarisk/README.md | `7d2d5177d763590ddd1508d2c91cab1f18d368684227cb4b7aa27f85a9a2e81c` |
| apis/tier8-new/cmsbl-halal/README.md | `dbcba107a2ed258661856c4f2f1b80447af1f0e15f8b1dd894fb21f9a8d80fe1` |
| apis/tier8-new/coretax/README.md | `1aa1c410fd729dd415709ce149e3b2eded3beb2be0451135ad21cb59be5ab94f` |
| apis/tier8-new/kpu/README.md | `69b9ff304651e75c4733c1d6e17fac9e5702f25522b8cda278d6c5e553431eec` |
| apis/tier8-new/satusehat/README.md | `7038522526afc204147ecb369b98def646c7d3328bad2ff0e6b74ddb422896dd` |
| apis/tier8-new/simbg/README.md | `7bbf35041d98d2a3ab7ac1e5bd72361ba1f1027fc4ae59cd2f320a3c2af69075` |
| docs/monitor-only-endpoints.md | `f2f059987b544183a0ca1a915eaa69af94b65995cd3ba3e1469abfa1fb9f2ec6` |
| docs/source-review-2026-10-10.md | `d65a7fd7942c4e57b5738bd6eea3511b675dd068ef6aaab38b34152c356fe159` |
| mcp-servers/README.md | `99a1328f79475ee26bf3e8299f7fefb63fc97aec94efe161fd11e0147b53517b` |
| references/bank-indonesia.md | `f85c16fd0b39c0887fb2050b16006cd5abf0f793751ef0dd2f9d888287f369b3` |
| references/bmkg-weather.md | `525413dc662b113c984aea7832026f380ad618db0a2f9c192e3260f238bb5724` |
| references/bpjph-halal.md | `a9ad5460c23e7865fec86ca3ad303986bca9c41c325bdcc0cf1aea5062208aac` |
| references/bpom-products.md | `36cbdf3b34c944fe067750490e77cbc1e5b6dd112dc42cd6d1c5b0e4825731cf` |
| references/bps-statistics.md | `f0a971d4858b566f0033a1c439116c9d9efecab8b0923832bf7a195dfd31a816` |
| references/ckan-portals.md | `d56b11e2a0da2e7128fb0472d3b7b976c5547488653de3b283afa8fe88bf6e70` |
| references/company-verification.md | `e8e637bb138f5bfa17ae20065c18bd241dc7a40bd99f638289f62be85c86ddea` |
| references/idx-stocks.md | `866988c01fcb9af6b6ad5c804d6a8e93176313566cc6a6d47750a2c49482e511` |
| references/inarisk-disaster.md | `3d72aa26953ea6edec70083e43f67b857d61aaab782d852b1e86f8d7a19872c4` |
| references/ojk-legality.md | `a27284b8150e3b66aeae3c50f392c12a68ab07a2abf865792d09090bef19a540` |
| references/pasal-id-law.md | `095ff77b5dacba0fa4078bc9546928dfacad0a7706d3628d81be4a74766ad6bd` |
| status/2026-03-29-update.md | `8cc66bd380591b93536a8350579797a00b9edeb39fdb790e1dfb1289e824eead` |
| status/2026-10-10-update.md | `0ba2d6c6107790764989c56d60bf5b15349c3693771f239891aaa80bf3b86c43` |
| status/README.md | `f44c7c7cce4f8b53e968256bed30383bdc1c93f2ed4d302ac6482800232d7136` |

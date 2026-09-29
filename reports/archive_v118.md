# V118: original Storm archive checked

The owner-linked [BO4CO deposit](https://zenodo.org/records/56238), DOI10.5281/zenodo.56238, was downloaded under a separate frozen 1 MiB allowance after the V116 source audit. Its API metadata explicitly identifies **BSD-3-Clause**; the 139,425-byte archive matches the published MD5 `c84ef2ba1d2e2500affa80b72ee38d98` and has SHA256 `d5196e128d514e42df3f525d357fb819d508a41e1833761eb3dcb96f4ab46d7f`. This resolves the earlier uncertainty about the deposit's stated license, without extending that license to unrelated artifacts.

The archive contains ten configuration/performance CSVs plus macOS file metadata. No per-attempt validation/failure log, workload correctness certificate or executed-code manifest is included. We enumerated members without extracting them, converted only configuration fields, and compared normalized feature sets with the existing MOOT registry. Neither objective column was converted, exported, ranked or used to select a table.

| Original member | Unique configurations | Feature-only MOOT match |
|---|---:|---|
| rs-6d-c3 | 3,840 | SS-J, SS-S, rs-6d-c3_obj1/obj2 |
| sol-6d-c2 | 2,866 | sol-6d-c2-obj1 |
| wc+rs-3d-c4 | 196 | Same feature space as all three multi-tenant tables and their aliases |
| wc+sol-3d-c4 | 196 | Same feature space as all three multi-tenant tables and their aliases |
| wc+wc-3d-c4 | 196 | Same feature space as all three multi-tenant tables and their aliases |
| wc-3d-c4 | 756 | SS-E |
| wc-5d-c5 | 1,080 | SS-I |
| wc-6d-c1 | 2,880 | SS-K, wc-6d-c1-obj1 |
| wc-c1-3d-c1 | 1,343 | SS-A |
| wc-c3-3d-c1 | 1,512 | SS-C |

The multi-tenant matches demonstrate why identical feature names/vectors cannot uniquely establish workload identity. Different co-located applications use the same configuration space. Likewise, matching a feature matrix does not prove target values, direction transformations or units agree. Original archive headers identify throughput and latency but cannot resolve the source-level metric substitutions found in V116. All topologies and cluster variants remain the **same Storm family**.

**Admission remains closed under the frozen V52 gates.** The archive resolved location, schema and stated licensing. It did not recover the missing run-level metric/validation/failure linkage. This is not a claim that the original dataset is invalid, nor evidence of unfavorable optimization outcomes: no performance comparison was made. Future work must either obtain the original measurement contract/linked records or explicitly design a fresh validated collection; do not silently convert this audit into a held-out experiment.

Both public retrievals succeeded, totaling 145,893 saved bytes including metadata. Zero model requests, optimizer acquisitions, native workloads or external spending. The V116/V118 combined new downloads are 436,802 bytes, leaving 861,078,321 bytes within the existing 10 GiB cumulative cap.

Evidence: `artifacts/sources/v118/`, `results/v118_archive/summary.json`, `artifacts/study_v118/`. Reproduce with `.venv/bin/python scripts/audit_archive_v118.py --verify-only`. Four synthetic tests check poisoned-target isolation, feature-signature invariance, unsafe archive member rejection and nonfinite inputs. They are not measured experiments.

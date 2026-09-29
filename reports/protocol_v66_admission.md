# V66 — legal proposal interface and fresh application utility admission

Do not repair, re-score or call models on V65 cases. Generalize a finite-domain
interface from earlier constrained decoding: one complete legal configuration per
request, removing acquired and previously proposed rows before constructing each
grammar. Independent acceptance rejects even a server grammar violation. Requests
are charged before transport, zero retries; failure terminates the batch. Classical
selectors get the same eligible configurations. Ten selections require ten real
requests; this cost cannot be hidden. Synthetic tests do not establish model quality
or that the local runtime obeys the grammar. No real inference is authorized here.

Audit and build DuckDB1.3.2 (owner PyPI wheel, MIT), GNU coreutils9.7 sort (owner
release archive, GPL3+), and OpenJPEG2.5.3 (owner commit210a8a5690d0da66f02d49420d7176a21ef409dc,
BSD2). Fixed versions selected for portable local feasibility, not latest-version
claims. Owner documentation and source options inspected before builds. Preserve
initial failed platform-tag/SDK/build-prerequisite attempts. No system install,
cloud, credentials, external extensions or downloaded installers. Source cap80MiB
within existing573+MiB remaining allowance; build process time600s total. No source
patches to application algorithms. Owner tar hash/HTTPS provenance is recorded;
the retrieved GNU signature is not independently key-verified.

Identifier audit of7725 saved research JSON/JSONL/manifests finds no candidate
matches; deleted/external/unidentified/unstructured history remains a blind spot.
Candidates are new development-admission groups, not certified untouched test data.
All related variants and seeds stay grouped. Do not combine these three groups into
a claimed sufficient held-out router evaluation.

Freeze inputs, grid and trial recipes before application timings. Generated workloads
are application inputs executed by real programs, distinct from synthetic unit tests
but not production/competition samples. Exactly one workload per candidate, no
adaptive size calibration or parameter-grid changes after outcomes:

- DuckDB: 2^22 fact rows with k=i%4096,g=i%256,v=i%97, joined to4096 dimension
  rows with w=k%17+1. Objective is first SELECT/group/sum/count/order execution and
  materialization time after loading, not database setup or Python startup. Every
  returned integer checked against independently generated Python sums/counts.
  External access/autoinstall/autoload disabled, insertion-order preservation false,
  private spill directory. Grid: threads[1,2,4,8],memory[64,128,256,512]MB,
  perfect-hash threshold[0,8,12],48settings. Reference[1,256MB,12],contrast[8,64MB,0].
- GNU sort: 2^20 unique padded decimal lines, fixed affine permutation; bytewise
  LC_ALL=C ascending order. Full output SHA must equal independently generated sorted
  sequence. Objective whole native process exit time, including input/output. Grid:
  parallel[1,2,4,8],buffer[1,4,16,64]MiB,batch[2,16,64],48settings. Reference[1,16M,16],
  contrast[8,1M,2]. Buffer size is a tuning hint, not a hard process-memory cap.
- OpenJPEG: fixed1024x1024 generated8-bit grayscale image. Reversible lossless
  encoding (-r1), exact decoded shape/maxval/every pixel. Objective encoder whole
  process exit time; decoder verification time is separate actual collection cost.
  Grid: block[16,32,64],resolutions[3,5],tile[128,256,512,1024],threads[1,2],48settings.
  Reference[64,5,1024,1],contrast[16,3,128,2]. Compressed sizes are recorded, not a
  post-hoc constraint; all outputs must preserve exact pixels.

Each family runs reference/contrast/reference, nine intended configuration trials,
fixed order DuckDB,sort,OpenJPEG. Up to12 application invocations including three
decoder validations, plus Python supervisors/workers. No performance acquisitions
are omitted because validation failed. Per trial45s outer wall, sampled1GiB RSS;
native encode/sort/decode children each20s and inherit the supervised worker group.
Stage600s, no launch with less than50s left. Stop remaining trials of a failing
family, retain unattempted denominator, continue independent families. No retries.

Admission requires all three intended trials valid. This checks implementation
feasibility and correctness, not stable speedup, optimizer headroom or LLM benefit.
Zero model requests, new recorded-table optimizer accesses, external spending or
automatic full-grid runs. Separate prospective full-grid protocol required before
timing remaining settings. No revisions based on favorable probe timings.

# Bounded archive inspection, before retrieving any member

The pinned latest owner record is version1.2, DOI10.5281/zenodo.7658046. Its
archive is401331220 bytes; do not fetch it in full under this metadata stage.
Use exact HTTP Range requests to inspect its ZIP central directory, then only
explicitly selected documentation, configuration/feature files or source scripts.
Reject a server that ignores Range before reading its body. Count every fetched
range together with previous metadata bodies against the SAME10MiB stage cap.
CRC-check extracted members and SHA256-pin their content and compressed ranges.
The full archive MD5 remains unverified until a separately authorized full fetch.
No objective member may be opened, and no extracted code may run. Persist the
complete filename/size/CRC inventory without inspecting performance rows.

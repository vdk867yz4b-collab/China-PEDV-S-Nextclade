param(
  [Parameter(Mandatory=$true)]
  [string]$Repo,
  [string]$Branch = "main"
)

$datasetPath = "nextclade_dataset_pedv_s_genbank_china_isolates"
$encoded = "gh:$Repo@$Branch@/$datasetPath"
"https://clades.nextstrain.org/?dataset-url=$encoded"

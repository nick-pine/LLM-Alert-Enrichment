rule ExampleMatch
{
    meta:
        description = "Matches alerts containing the word 'malware'"
    strings:
        $malware = "malware"
    condition:
        $malware
}

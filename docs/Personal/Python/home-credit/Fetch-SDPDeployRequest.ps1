<#
    .SYNOPSIS
    Invokes sqlcmd utility to run servicedesk.dbo.DeploymentReport sp to fetch all Deploy request tickets

    .DESCRIPTION
    Invokes sqlcmd utility to run servicedesk.dbo.DeploymentReport sp to fetch all Deploy request tickets

    .OUTPUTS
    Deploy Request tickets saved in xls format 

    .EXAMPLE
    .\Fetch-SDPDeployRequest.ps1 -myServerInstance 'IIV-CO-SQL03.PH.ESL-ASIA.COM,1433' -myUsername 'jenkinsuser' –myPassword '********' -StartDate '05/25/2017' -EndDate '05/30/2017'

    .NOTES
    Created By Jen Gregorio - 05/25/2017
#> 
Param (                    
    [Parameter(Mandatory=$True)]      
    [string]$myServerInstance,    

    [Parameter(Mandatory=$True)]      
    [string]$myUsername,

    [Parameter(Mandatory=$True)]      
    [string]$myPassword,
   
    [Parameter(Mandatory=$False)]      
    [string]$StartDate,

    [Parameter(Mandatory=$False)]      
    [string]$EndDate,

    [Parameter(Mandatory=$False)]      
    [string]$RequestType,

    [Parameter(Mandatory=$False)]      
    [string]$OutputPath = '.\Release.xls'
)
Clear-Host
"`r`n`r`n`r`n"

#Start Stopwatch  
$sw = [Diagnostics.Stopwatch]::StartNew()
"***Started at $(Get-Date)"

    function StopWatch
    {
        #Stop Stopwatch  
        $sw.Stop()
        "`r`n`r`n***Ended at $(Get-Date)"
        "***Total Elapsed Time: $($sw.Elapsed.ToString())"
    }
        


    if ($StartDate -eq "")
    {
        $StartDate = (Get-date).AddDays(-7).ToString("MM/dd/yyyy")
    }

    if ($EndDate -eq "")
    {
        $EndDate = (Get-date).AddDays(+30).ToString("MM/dd/yyyy")
    }    
    
            
    try
    {
        "Fetching Deploy Request ticket from SDP database..."
        if ($RequestType -eq 'RM')
        {
            $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'|' -Q "set nocount on; EXEC servicedesk.dbo.TaskDeploymentReport @p_type = 'RM', @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath   
        }
        #elseif ($RequestType -eq 'DB')
        #{
        #   $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'|' -Q "set nocount on; EXEC servicedesk.dbo.TaskDeploymentReport @p_type = 'DB', @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath   
        #}
        elseif ($RequestType -eq 'Change')
        {
            $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'~' -Q "set nocount on; EXEC SDP.dbo.SDP_ChangeRequest_RM @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath   
        }
        elseif ($RequestType -eq 'ChangeNewSDP')
        {
            $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'~' -Q "set nocount on; EXEC servicedesk.dbo.SDP_ChangeRequest_RM @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath   
        }
    elseif ($RequestType -eq 'ChangeNewSDP2')
        {
            $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'~' -Q "set nocount on; EXEC servicedesk.dbo.SDP_ChangeRequest_RM_NEW @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath   
        }
        else
        {
            $MyOutput = & "C:\Program Files (x86)\Red Gate\sqlCI\sqlCmd\x64\sqlcmd.exe" -S $myServerInstance -U $myUsername -P $myPassword -b -m-1 -t600 -r1 -s'|' -Q "set nocount on; EXEC servicedesk.dbo.DeploymentReport @p_DateFrom = '$StartDate', @p_DateTo = '$EndDate'" -I -o $OutputPath    
        }
    }    
    catch [System.Net.WebException],[System.Exception]
    {
        $Error[0].Exception.Message
    }
    finally
    {        
        if ($?)
        {
            "Successfully saved in $OutputPath"
        }

Francis Paolo Cruz, [12.02.19 16:16]
StopWatch
    }


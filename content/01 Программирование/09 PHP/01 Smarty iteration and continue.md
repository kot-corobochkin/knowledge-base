{foreach from=$fullReport item=foundRecord key=paramName}
    {continue if $paramName == 'statuses'}

    ... your code ...
{/foreach}
function approvalOnLoad()
{​​​​​​​
debugger;
var initiator=Xrm.Page.getAttribute("qbd_employee").getValue();
var typecategory=Xrm.Page.getAttribute("qbd_typecategory").getValue();

    if(initiator != null){​​​​​​​
    Xrm.Page.ui.tabs.get("General").setVisible(true);
    }​​​​​​​
    else if(typecategory != null)
    {​​​​​​​
    Xrm.Page.ui.tabs.get("General").setVisible(true);
    }​​​​​​​
}​​​​​​​
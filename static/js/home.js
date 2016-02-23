$(document).ready(function () {

    refresh()
    // Hide forms
    hideForms()
    // Button click handling
    setDeletionForm()
    setEditionForm()
    setCreationForm()
    // Confirmation actions
    setDeleteAction()
    setCreateAction()
    setEditAction()

});

// Dynatable functions

function refresh() {
    var $dynamic_table = $("#home-dtable");
    $.ajax({
        type: 'GET',
        url: '/api/applications_list/',
        dataType: "json",
        success: function (data) {
            $dynamic_table.dynatable({
                dataset: {
                    records: data
                },
                features: {
                    pushState: false
                }
            });
            table_refresh(data)
        }
    });
}

function table_refresh(data) {
    var dynatable = $('#home-dtable').data("dynatable");
    dynatable.records.updateFromJson({records: data});
    dynatable.records.init();
    dynatable.process();
    //dynatable.dom.update();
}

// Button handlings
function setDeletionForm() {
    $("#deletions").click(function () {
        removeHiglightFromChecked()
        $("#deletions").addClass("home-form-button-highlited");
        $("#deletions-form").show("slow");

        $("#edition").removeClass("home-form-button-highlited");
        $("#edition-form").hide("slow");

        $("#creation").removeClass("home-form-button-highlited");
        $("#creation-form").hide("slow");
    })
}

function setEditionForm() {
    $("#edition").click(function () {
        removeHiglightFromChecked()
        $("#deletions").removeClass("home-form-button-highlited");
        $("#deletions-form").hide("slow");

        $("#edition").addClass("home-form-button-highlited");
        $("#edition-form").show("slow");

        $("#creation").removeClass("home-form-button-highlited");
        $("#creation-form").hide("slow");
    })
}

function setCreationForm() {
    $("#creation").click(function () {
        removeHiglightFromChecked()

        $("#deletions").removeClass("home-form-button-highlited");
        $("#deletions-form").hide("slow");

        $("#edition").removeClass("home-form-button-highlited");
        $("#edition-form").hide("slow");

        $("#creation").addClass("home-form-button-highlited");
        $("#creation-form").show("slow");
    })
}

function hideForms() {
    $("#deletions-form").hide();
    $("#edition-form").hide();
    $("#creation-form").hide()
}

function trmouseclick(i) {
    var deletion = $("#deletions-form").is(":visible")

    var creation = $("#creation-form").is(":visible")
    if (creation == true) {
        return;
    }

    var edition = $("#edition-form").is(":visible")
    if (edition == true) {
        var uid = return_checked();
        getInformationToEdtitionForm(uid);
        removeHiglightFromChecked()
        var row = $("tr").get(i.rowIndex);
        row.className = "mouseover";
        return;
    }

    if (deletion == false && creation == false && edition == false)
        return;

    var row = $("tr").get(i.rowIndex);
    if (row.className == "mouseover")
        row.className = "";
    else
        row.className = "mouseover";
    var ids = document.getElementsByClassName("mouseover");
}

function return_checked() {
    var ret_ids = [];
    var ids = document.getElementsByClassName("mouseover");
    for (var i = 0; i < ids.length; i++)
        ret_ids.push(ids.item(i).firstChild.textContent);
    return ret_ids;
}

function removeHiglightFromChecked() {
    $(".mouseover").removeClass("mouseover");
}

// Delete

function setDeleteAction() {
    $("#button_delete").click(function () {
        deleteSelected(return_checked())
    })
}

function setCreateAction() {
    $("#button_create").click(function () {
        addNewPostition()
    })
}

function setEditAction() {
    $("#edition_button_create").click(function () {
        confirmEdition(return_checked()[0])
    })
}

// Api calls

function deleteSelected(ids) {
    for (var i = 0; i < ids.length; i++) {
        var url = '/api/application_detail/' + ids[i].toString() + '/';
        $.ajax({
            type: 'DELETE',
            url: url,
            dataType: "json",
            success: function (data) {
                refresh()
            }
        })
    }
}

function addNewPostition() {
    // TODO VALIDATION!!
    var jsonObject = new Object()

    jsonObject.applicationNumber = $("#applicationNumber").val()
    jsonObject.applicationOwner = $("#applicationOwner").val()
    jsonObject.applicationTitle = $("#applicationTitle").val()
    jsonObject.firstViewBy = $("#firstViewBy").val()
    jsonObject.secondViewBy = $("#secondViewBy").val()
    jsonObject.firstStageOpinion = $("#firstStageOpinion").val()
    jsonObject.additionalDescription = $("#additionalDescription").val()

    var url = '/api/applications_list/'
    $.ajax({
        type: 'POST',
        url: url,
        dataType: "json",
        data: jsonObject,
        success: function (data) {
            refresh();
        }
    })
}

function getInformationToEdtitionForm(id) {
    var url = '/api/application_detail/' + id.toString() + '/';
    $.ajax({
        type: 'GET',
        url: url,
        dataType: "json",
        success: function (data) {
            $("#editionApplicationNumber").val(data.applicationNumber);
            $("#editionApplicationOwner").val(data.applicationOwner);
            $("#editionApplicationTitle").val(data.applicationTitle);
            $("#editionFirstViewBy").val(data.firstViewBy);
            $("#editionSecondViewBy").val(data.secondViewBy);
            $("#editionFirstStageOpinion").val(data.firstStageOpinion);
            $("#editionAdditionalDescription").val(data.additionalDescription);
            refresh();
        }
    })
}

function confirmEdition(id) {
    if (id == null)
        return;
    var jsonObject = new Object()

    jsonObject.applicationNumber = $("#editionApplicationNumber").val()
    jsonObject.applicationOwner = $("#editionApplicationOwner").val()
    jsonObject.applicationTitle = $("#editionApplicationTitle").val()
    jsonObject.firstViewBy = $("#editionFirstViewBy").val()
    jsonObject.secondViewBy = $("#editionSecondViewBy").val()
    jsonObject.firstStageOpinion = $("#editionFirstStageOpinion").val()
    jsonObject.additionalDescription = $("#editionAdditionalDescription").val()

    var url = '/api/application_detail/' + id.toString() + '/';
    $.ajax({
        type: 'PUT',
        url: url,
        dataType: "json",
        data: jsonObject,
        success: function (data) {
            refresh();
        }
    })
}
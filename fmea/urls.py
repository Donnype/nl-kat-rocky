from django.urls import path
from fmea import views

urlpatterns = [
    path("", views.FMEAIndexView.as_view(), name="fmea_intro"),
    path(
        "failure-modes/create/",
        views.FailureModeCreateView.as_view(),
        name="fmea_failure_mode_create",
    ),
    path(
        "failure-modes/",
        views.FailureModeListView.as_view(),
        name="fmea_failure_mode_list",
    ),
    path(
        "failure-modes/effects/create/",
        views.FailureModeEffectCreateView.as_view(),
        name="fmea_failure_mode_effect_create",
    ),
    path(
        "failure-modes/effects/",
        views.FailureModeEffectListView.as_view(),
        name="fmea_failure_mode_effect_list",
    ),
    path(
        "failure-modes/affected-objects/create/",
        views.FailureModeAffectedObjectCreateView.as_view(),
        name="fmea_failure_mode_affected_object_create",
    ),
    path(
        "failure-modes/affected-objects/<pk>/update/",
        views.FailureModeAffectedObjectUpdateView.as_view(),
        name="fmea_failure_mode_affected_object_update",
    ),
    path(
        "failure-modes/affected-objects/",
        views.FailureModeAffectedObjectListView.as_view(),
        name="fmea_failure_mode_affected_object_list",
    ),
    path(
        "failure-modes/affected-objects/<pk>/",
        views.FailureModeAffectedObjectDetailView.as_view(),
        name="fmea_failure_mode_affected_object_detail",
    ),
    path(
        "failure-modes/department-heatmap/",
        views.FMEADepartmentHeatmapView.as_view(),
        name="fmea_department_heatmap",
    ),
    path(
        "failure-modes/<pk>/",
        views.FailureModeDetailView.as_view(),
        name="fmea_failure_mode_detail",
    ),
    path(
        "failure-modes/<pk>/report/",
        views.FailureModeReportView.as_view(),
        name="fmea_failure_mode_report",
    ),
    # path(
    #     "failure-modes/<pk>/report/pdf/",
    #     views.GenerateFailureModePDF.as_view(),
    #     name="fmea_failure_mode_report_pdf",
    # ),
    path(
        "failure-modes/<pk>/update/",
        views.FailureModeUpdateView.as_view(),
        name="fmea_failure_mode_update",
    ),
    path(
        "fmea_node_selection/",
        views.FMEATreeObjectView.as_view(),
        name="fmea_node_selection",
    ),
    path(
        "failure-modes/effects/<pk>/",
        views.FailureModeEffectDetailView.as_view(),
        name="fmea_failure_mode_effect_detail",
    ),
    path(
        "failure-modes/effects/<pk>/update/",
        views.FailureModeEffectUpdateView.as_view(),
        name="fmea_failure_mode_effect_update",
    ),
]

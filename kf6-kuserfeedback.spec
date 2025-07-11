%define major %(echo %{version} |cut -d. -f1-2)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname KF6UserFeedbackCore
%define devname %mklibname KF6UserFeedbackCore -d
%define wlibname %mklibname KF6UserFeedbackWidgets
%define wdevname %mklibname KF6UserFeedbackWidgets -d
#define git 20240217

Name: kf6-kuserfeedback
Version: 6.16.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/kuserfeedback/-/archive/master/kuserfeedback-master.tar.bz2#/kuserfeedback-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/frameworks/%{major}/kuserfeedback-%{version}.tar.xz
%endif
Summary: Library for collecting user feedback
URL: https://invent.kde.org/frameworks/kuserfeedback
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6Charts)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: cmake(Qt6Help)
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: gperf
BuildRequires: bison
BuildRequires: flex
BuildRequires: php-cli
BuildRequires: qdoc
BuildRequires: qt6-qtbase-doc
Requires: %{libname} = %{EVRD}

%description
Library for collecting user feedback

%package -n %{libname}
Summary: Library for collecting user feedback
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Library for collecting user feedback

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

KUserFeedback is a library for collecting user feedback.

%package -n %{wlibname}
Summary: Library for collecting user feedback (GUI components)
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{wlibname}
Library for collecting user feedback (GUI components)

%package -n %{wdevname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{devname} = %{EVRD}
Requires: %{wlibname} = %{EVRD}

%description -n %{wdevname}
Development files (Headers etc.) for %{name}.

KUserFeedback is a library for collecting user feedback.
This package provides the development files for the GUI components.

%prep
%autosetup -p1 -n kuserfeedback-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

D="$(pwd)"
# FIXME %%find_lang doesn't do the right thing for QM files inside LC_MESSAGES
# So for now, let's do its job manually
cd %{buildroot}%{_datadir}/locale
for i in *; do
	[ -e $i/LC_MESSAGES/userfeedbackprovider6_qt.qm ] && echo "%%lang($i) %{_datadir}/locale/$i/LC_MESSAGES/userfeedbackprovider6_qt.qm" >>$D/%{name}.lang
done

# Userfeedbackconsole seems to be gone, so no need for its docs and translations either...
rm -rf %{buildroot}%{_datadir}/KDE \
	%{buildroot}%{_datadir}/locale/*/LC_MESSAGES/userfeedbackconsole6_qt.qm


%files -f %{name}.lang
%{_datadir}/qlogging-categories6/org_kde_UserFeedback.categories

%files -n %{devname}
%{_includedir}/KF6/KUserFeedback
%{_includedir}/KF6/KUserFeedbackCore
%{_libdir}/cmake/KF6UserFeedback
%{_qtdir}/mkspecs/modules/qt_KF6UserFeedbackCore.pri

%files -n %{libname}
%{_libdir}/libKF6UserFeedbackCore.so*
%{_qtdir}/qml/org/kde/userfeedback

%files -n %{wlibname}
%{_libdir}/libKF6UserFeedbackWidgets.so*

%files -n %{wdevname}
%{_includedir}/KF6/KUserFeedbackWidgets
%{_qtdir}/mkspecs/modules/qt_KF6UserFeedbackWidgets.pri

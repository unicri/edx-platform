"""
Single page accessibility tests for LMS.
"""
import os

from bok_choy.browser import save_source
from django.conf import settings

from ..pages.lms.auto_auth import AutoAuthPage
from ..pages.lms.courseware import CoursewarePage
from ..pages.lms.dashboard import DashboardPage
from ..pages.lms.course_info import CourseInfoPage
from ..pages.lms.login import LoginPage
from ..pages.lms.progress import ProgressPage
from ..pages.common.logout import LogoutPage
from ..fixtures.course import CourseFixture, XBlockFixtureDesc, CourseUpdateDesc
from ..tests.helpers import UniqueCourseTest, load_data_str

class LmsAccessibilityTest(UniqueCourseTest):
    """
    Base class to capture LMS accessibility scores
    """
    username = 'test_student'
    email = 'student101@example.com'

    REPO_DIR = os.getcwd()
    os.environ['SAVED_SOURCE_DIR'] = '{}/test_root/log/auto_screenshots'.format(REPO_DIR)

    def setUp(self):
        """
        Setup course
        """
        super(LmsAccessibilityTest, self).setUp()

        # Install a course with sections/problems, tabs, updates, and handouts
        course_fix = CourseFixture(
            self.course_info['org'], self.course_info['number'],
            self.course_info['run'], self.course_info['display_name']
        )

        course_fix.add_update(CourseUpdateDesc(date='January 29, 2014', content='Test course update1'))
        course_fix.add_update(CourseUpdateDesc(date='January 30, 2014', content='Test course update2'))
        course_fix.add_update(CourseUpdateDesc(date='January 31, 2014', content='Test course update3'))

        course_fix.add_children(
            XBlockFixtureDesc('chapter', 'Test Section 1').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 1').add_children(
                    XBlockFixtureDesc('problem', 'Test Problem 1', data=load_data_str('multiple_choice.xml')),
                    XBlockFixtureDesc('problem', 'Test Problem 2', data=load_data_str('formula_problem.xml')),
                    XBlockFixtureDesc('html', 'Test HTML', data="<html>Html child text</html>"),
                )
            ),
            XBlockFixtureDesc('chapter', 'Test Section 2').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 2').add_children(
                    XBlockFixtureDesc('html', 'Html Child', data="<html>Html child text</html>")
                )
            ),
            XBlockFixtureDesc('chapter', 'Test Section 3').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection 3').add_children(
                    XBlockFixtureDesc('problem', 'Test Problem 3')
                )
            )
        ).install()

        AutoAuthPage(self.browser, username=self.username, email=self.email, course_id=self.course_id).visit()

    def _capture_page_source(self, page):
        """
        Visit page and capture the page source.
        """
        source_name = '{page}_{course}'.format(page=type(page).__name__, course=self.course_info['number'])
        page.visit()
        from nose.tools import set_trace; set_trace()
        save_source(self.browser, source_name)

    def test_visit_courseware(self):
        courseware_page = CoursewarePage(self.browser, self.course_id)
        self._capture_page_source(courseware_page)

    def test_visit_dashboard(self):
        dashboard_page = DashboardPage(self.browser)
        self._capture_page_source(dashboard_page)

    def test_visit_course_info(self):
        course_info_page = CourseInfoPage(self.browser, self.course_id)
        self._capture_page_source(course_info_page)

    def test_visit_login_page(self):
        login_page = LoginPage(self.browser)

        # Logout previously logged in user to be able to see Login page.
        LogoutPage(self.browser).visit()
        self._capture_page_source(login_page)

    def test_visit_progress_page(self):
        progress_page = ProgressPage(self.browser, self.course_id)
        self._capture_page_source(progress_page)

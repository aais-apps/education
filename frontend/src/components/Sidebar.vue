<template>
  <div
    class="flex h-full flex-col justify-between transition-all duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-56'"
  >
    <div class="flex flex-col overflow-hidden">
      <UserDropdown
        class="p-2"
        :isCollapsed="isSidebarCollapsed"
        :educationSettings="
          !educationSettings.loading && educationSettings.data
        "
      />
      <div
        v-if="isStudent || activeStudentId"
        class="flex flex-col overflow-y-auto"
      >
        <SidebarLink
          :label="link.label"
          :to="link.to"
          v-for="link in links"
          :key="link.to"
          :isCollapsed="isSidebarCollapsed"
          :icon="link.icon"
          :isExternal="link.isExternal"
          class="mx-2 my-0.5"
        />

        <SidebarLink
          v-show="isGuardian"
          :label="__('View Students')"
          :to="'/students'"
          :isCollapsed="isSidebarCollapsed"
          :icon="Users"
          :isRedirect="true"
          class="mx-2 my-0.5"
        />
      </div>
    </div>
    <SidebarLink
      :label="__(isSidebarCollapsed ? 'Expand' : 'Collapse')"
      :isCollapsed="isSidebarCollapsed"
      @click="isSidebarCollapsed = !isSidebarCollapsed"
      class="m-2"
    >
      <template #icon>
        <span class="grid h-5 w-6 flex-shrink-0 place-items-center">
          <ArrowLeftToLine
            class="h-4.5 w-4.5 text-gray-700 duration-300 ease-in-out"
            :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }"
          />
        </span>
      </template>
    </SidebarLink>
  </div>
</template>

<script setup>
import { __ } from '@/translation'
import { storeToRefs } from 'pinia'
import { useStorage } from '@vueuse/core'
import SidebarLink from '@/components/SidebarLink.vue'
import {
  LayoutDashboard,
  CalendarCheck,
  GraduationCap,
  Banknote,
  UserCheck,
  ArrowLeftToLine,
  BookOpen,
  Users,
} from 'lucide-vue-next'

import UserDropdown from './UserDropdown.vue'
import { createResource } from 'frappe-ui'
import { portalStore } from '@/stores/portal'
import Button from 'frappe-ui/src/components/Button.vue'

const links = [
  // {
  // 	label: 'Dashboard',
  // 	to: '/',
  // 	icon: LayoutDashboard,
  // },
  {
    label: __('Schedule'),
    to: '/schedule',
    icon: CalendarCheck,
  },
  {
    label: __('Grades'),
    to: '/grades',
    icon: GraduationCap,
  },
  {
    label: __('Fees'),
    to: '/fees',
    icon: Banknote,
  },
  {
    label: __('Attendance'),
    to: '/attendance',
    icon: UserCheck,
  },
  {
    label: __('Online Learning'),
    to: '/lms',
    icon: BookOpen,
    isExternal: true,
  },
  // {
  // 	// TODO: create School Diary Page with card like CRM and from ListView go to Resource Document of each Card
  // 	label: 'Notes',
  // 	to: '/notes',
  // 	icon: BookOpen,
  // },
  // {
  // 	label: 'Profile',
  // 	to: '/profile',
  // 	icon: User,
  // },
]

const isSidebarCollapsed = useStorage('sidebar_is_collapsed', false)

// create a resource which call the function get_school_abbr_logo in api file using createResource
const educationSettings = createResource({
  url: 'education.education.api.get_school_abbr_logo',
  auto: true,
})

const store = portalStore()
const { isStudent, isGuardian, activeStudentId } = storeToRefs(store)
</script>

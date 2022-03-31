import { shallowMount } from '@vue/test-utils';
import CentralMap from '@/components/CentralMap.vue';

describe('CentralMap.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message';
    const wrapper = shallowMount(CentralMap, {
      propsData: { msg },
    });
    expect(wrapper.text()).toMatch(msg);
  });
});

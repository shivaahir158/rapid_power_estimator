import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
//import 'isomorphic-fetch';
import DeviceList from '../components/DeviceList';
import { SelectionProvider } from '../SelectionProvider';
import { SocTotalPowerProvider } from '../SOCTotalPowerProvider';
import { GlobalStateProvider } from '../GlobalStateProvider';

describe('DeviceList', () => {
  it('default value', () => {
    const { getByLabelText } = render(
      <GlobalStateProvider>
        <SocTotalPowerProvider>
          <SelectionProvider>
            <DeviceList devices={[{ id: 'test-dev', series: 'test' }]} setDevice={(dev) => { }} />
          </SelectionProvider>
        </SocTotalPowerProvider>
      </GlobalStateProvider>,
    );
    expect(getByLabelText('Device:')).toBeInTheDocument();
    expect(screen.getByText('test-dev test')).toBeInTheDocument();
    expect(screen.getByRole('combobox')).toHaveValue('selectDev');
  });
  it('select device', async () => {
    const user = userEvent.setup();
    render(
      <SocTotalPowerProvider>
        <SelectionProvider>
          <DeviceList devices={[{ id: 'test-dev', series: 'test' }]} setDevice={(dev) => { }} />
        </SelectionProvider>
      </SocTotalPowerProvider>,
    );
    // todo, need rework compoment since fetch
    // await user.selectOptions(screen.getByRole('combobox'), 'test-dev');
    // expect(screen.getByRole('option', { name: 'test-dev test' }).selected).toBe(true);
  });
});
